"""
pipeline_etl.py
===============
Pipeline ETL : Clinique du Sommeil d'Arles.
Version pandas.

Traite une nuit d'étude polysomnographique :
  1. EXTRACT   : lecture du CSV capteur avec pandas
  2. TRANSFORM : calcul des indicateurs cliniques avec pandas
  3. LOAD      : appel procédure sp_creer_resultat_nuit (écriture),
                 puis sp_lire_resultat_nuit (lecture pour rapport),
                 génération des courbes + rapport médical,
                 alimentation du datalake SQLite

Convention de nommage des fichiers capteur :
    signal_psg_patient_<id_patient>_nuit_<id_nuit>.csv

Dépendances :
    pip install pandas mysql-connector-python matplotlib --break-system-packages

Usage :
    python pipeline_etl_pandas.py <id_nuit>
"""

import os
import sys
import shutil
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error as MySQLError
from mdp import motdepasse, bdd, port


# ============================================================
# CONFIGURATION
# ============================================================
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": motdepasse,
    "database": bdd,
    "port": port
}

DATALAKE_PATH = "datalake.db"
#DUREE_NUIT_MIN = 420  # 7h : durée réelle de la nuit


# ============================================================
# UTILITAIRE : retrouver le CSV depuis l'id_nuit
# ============================================================
DOSSIER_RAW = "raw"


def trouver_csv_depuis_id_nuit(id_nuit, dossier_raw=DOSSIER_RAW):
    """
    Retrouve le chemin du CSV capteur à partir du seul id_nuit.

    Convention de nommage attendue :
        signal_psg_patient_<id_patient>_nuit_<id_nuit>.csv
    Exemple : signal_psg_patient_1_nuit_1.csv -> id_nuit=1

    On cherche dans le dossier raw/ le fichier qui se termine par
    "_nuit_<id_nuit>.csv", sans avoir besoin de connaître id_patient.

    Retourne
    --------
    (chemin_complet, id_patient)
    """
    suffixe_recherche = f"-nuit-{id_nuit}.csv"

    fichiers_trouves = [
        f for f in os.listdir(dossier_raw)
        if f.endswith(suffixe_recherche)
    ]

    if not fichiers_trouves:
        raise FileNotFoundError(
            f"Aucun fichier CSV trouvé pour id_nuit={id_nuit} "
            f"dans le dossier '{dossier_raw}/'. "
            f"Format attendu : signal-psg-patient-<id_patient>-nuit-{id_nuit}.csv"
        )

    if len(fichiers_trouves) > 1:
        raise ValueError(
            f"Plusieurs fichiers correspondent à id_nuit={id_nuit} : "
            f"{fichiers_trouves}. Vérifiez qu'il n'y a pas de doublon."
        )

    nom_fichier = fichiers_trouves[0]
    chemin_complet = os.path.join(dossier_raw, nom_fichier)

    # Extraction de id_patient depuis le nom : signal_psg_patient_<id>_nuit_<id>.csv
    nom_sans_extension = nom_fichier.replace(".csv", "")
    morceaux = nom_sans_extension.split("-")
    try:
        id_patient = int(morceaux[3])  # signal[0] psg[1] patient[2] <id>[3] nuit[4] <id>[5]
    except (IndexError, ValueError):
        raise ValueError(
            f"Impossible d'extraire id_patient depuis '{nom_fichier}'. "
            f"Format attendu : signal-psg-patient-<id_patient>-nuit-<id_nuit>.csv"
        )

    return chemin_complet, id_patient


# ============================================================
# 1) EXTRACT : lecture du CSV avec pandas
# ============================================================
def lire_csv_capteur(chemin_fichier):
    """
    Lit le CSV capteur avec pandas et retourne un DataFrame.

    Colonnes attendues :
        timestamp_sec, spo2, debit_nasal_pct, effort_thoracique_pct,
        position, ronflements_db, flag_evenement

    Lève
    ----
    FileNotFoundError : si le fichier n'existe pas
    ValueError : si le fichier est vide ou si des colonnes manquent
    """
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")

    df = pd.read_csv(chemin_fichier)

    if df.empty:
        raise ValueError(f"Le fichier {chemin_fichier} est vide.")

    # Vérification des colonnes attendues : évite un message d'erreur
    # cryptique plus tard dans le pipeline si une colonne est mal nommée
    colonnes_obligatoires = {
        "timestamp_sec", "spo2", "debit_nasal_pct",
        "effort_thoracique_pct", "position", "ronflements_db", "flag_evenement"
    }
    colonnes_manquantes = colonnes_obligatoires - set(df.columns)
    if colonnes_manquantes:
        raise ValueError(
            f"Colonnes manquantes dans {chemin_fichier} : {colonnes_manquantes}"
        )

    return df


# ============================================================
# 2) TRANSFORM : calcul des indicateurs avec pandas
# ============================================================
def calculer_indicateurs_signal(df, duree_nuit_min):
    """
    Calcule les indicateurs cliniques depuis le DataFrame du signal,
    puis extrapole les grandeurs cumulatives sur la nuit complète.

    Ne calcule PAS l'IAH ni les comptages d'événements (apnées,
    hypopnées, RERA) : c'est la responsabilité de la procédure
    stockée creer_resultat_nuit, qui requête evenement_respiratoire.
    On ne fait jamais d'INSERT direct dans resultat_nuit ici.

    Optimisation : chaque colonne n'est parcourue qu'une seule fois.
    Au lieu d'enchaîner .min(), .mean(), .median() (3 passages
    séparés sur la même colonne), on utilise .agg() qui calcule
    les trois en un seul passage vectorisé. Important si le CSV
    grossit (ex: passage de 1h à plusieurs heures de signal).

    Paramètres
    ----------
    df : DataFrame : sortie de lire_csv_capteur()
    duree_nuit_min : int : durée réelle de la nuit (ex: 420 pour 7h)

    Retourne
    --------
    dict avec les indicateurs prêts à être passés à la procédure.
    """
    # Pas d'échantillonnage entre deux lignes (ex: 10 secondes)
    pas_sec = df["timestamp_sec"].iloc[1] - df["timestamp_sec"].iloc[0]

    # Durée couverte par le CSV (ex: 3600 sec = 1h)
    duree_fenetre_sec = df["timestamp_sec"].iloc[-1] - df["timestamp_sec"].iloc[0] + pas_sec
    duree_sommeil_min = duree_fenetre_sec / 60
   

    # Facteur d'extrapolation : nuit complète / fenêtre CSV (ex: 7h/1h = 7)
    #facteur = duree_nuit_min / duree_fenetre_min

    # --- Statistiques SpO2 et ronflements en un seul appel .agg() ---
    # Un dict {colonne: [fonctions]} permet de calculer toutes les
    # statistiques nécessaires sur les deux colonnes en un seul appel,
    # pandas optimise l'exécution en interne.
    stats = df.agg({
        "spo2": ["min", "mean", "median"],
        "ronflements_db": ["max", "mean"],
    })

    spo2_min = round(stats.loc["min", "spo2"], 1)
    spo2_moy = round(stats.loc["mean", "spo2"], 1)
    spo2_mediane = round(stats.loc["median", "spo2"], 1)

    decibels_max = round(stats.loc["max", "ronflements_db"], 1)
    decibels_moy = round(stats.loc["mean", "ronflements_db"], 1)

    # --- Position dominante = valeur la plus fréquente (mode) ---
    position_dominante = df["position"].mode()[0]

    # --- Hypoxie + ronflements forts : un seul passage par colonne ---
    # (df["spo2"] < 90) crée un masque booléen en un seul parcours,
    # .sum() compte directement sur ce masque (pas de second parcours
    # de la colonne spo2 elle-même)
    nb_lignes_hypoxie = (df["spo2"] < 90).sum()
    nb_ronflements_forts_csv = (df["ronflements_db"] > 70).sum()

    duree_hypoxie_min_csv = (nb_lignes_hypoxie * pas_sec) / 60
    duree_hypoxie_min = round(duree_hypoxie_min_csv , 1)
    nb_ronflements_forts = round(nb_ronflements_forts_csv )

    return {
        "spo2_min": spo2_min,
        "spo2_moy": spo2_moy,
        "spo2_mediane": spo2_mediane,
        "decibels_max": decibels_max,
        "decibels_moy": decibels_moy,
        "position_dominante": position_dominante,
        "duree_hypoxie_min": duree_hypoxie_min,
        "nb_ronflements_forts": nb_ronflements_forts,
        "duree_sommeil_min": duree_sommeil_min
    }


def diagnostic_depuis_iah(iah):
    """Retourne le libellé de sévérité clinique selon l'IAH."""
    if iah < 5:
        return "Normal (pas de SAHOS)"
    elif iah < 15:
        return "SAHOS léger"
    elif iah < 30:
        return "SAHOS modéré"
    else:
        return "SAHOS sévère"


# ============================================================
# 3) LOAD : écriture en base (procédure sp_creer_resultat_nuit)
# ============================================================
def ecrire_resultat_nuit(id_nuit, id_medecin_validateur, indicateurs):
    """
    Appelle la procédure stockée sp_creer_resultat_nuit pour insérer
    (ou mettre à jour) le résultat de la nuit. La procédure se
    charge elle-même de requêter evenement_respiratoire pour
    calculer les comptages, l'IAH et les micro-éveils.

    On ne fait jamais d'INSERT direct dans resultat_nuit depuis Python.

    Lève
    ----
    RuntimeError : si l'appel à la procédure échoue côté MySQL
    """
    connexion = None
    try:
        connexion = mysql.connector.connect(**MYSQL_CONFIG)
        curseur = connexion.cursor(dictionary=True)

        curseur.callproc("sp_creer_resultat_nuit", [
            id_nuit,
            id_medecin_validateur,
            indicateurs["spo2_min"],
            indicateurs["spo2_moy"],
            indicateurs["spo2_mediane"],
            indicateurs["duree_hypoxie_min"],
            indicateurs["position_dominante"],
            indicateurs["decibels_max"],
            indicateurs["decibels_moy"],
            indicateurs["nb_ronflements_forts"],
            indicateurs["duree_sommeil_min"]
            
        ])

        # Récupération du SELECT de vérification renvoyé par la procédure
        confirmation = None
        for jeu_resultat in curseur.stored_results():
            confirmation = jeu_resultat.fetchone()

        connexion.commit()
        curseur.close()
        return confirmation

    except MySQLError as erreur:
        raise RuntimeError(
            f"Erreur MySQL lors de l'appel à sp_creer_resultat_nuit "
            f"pour id_nuit={id_nuit} : {erreur}"
        ) from erreur

    finally:
        if connexion is not None and connexion.is_connected():
            connexion.close()


# ============================================================
# 4) LOAD : lecture du résultat pour le rapport
# ============================================================
def lire_resultat_nuit(id_nuit):
    """
    Appelle la procédure sp_lire_resultat_nuit pour récupérer
    toutes les infos nécessaires au rapport médical (identité
    patient, contexte nuit, résultat complet) en un seul appel.

    On ne fait jamais de SELECT brut sur les tables depuis Python :
    la lecture passe toujours par cette procédure, comme l'écriture
    passe toujours par sp_creer_resultat_nuit.

    Lève
    ----
    RuntimeError : si l'appel à la procédure échoue côté MySQL
    ValueError : si aucun résultat n'existe pour cet id_nuit
    """
    connexion = None
    try:
        connexion = mysql.connector.connect(**MYSQL_CONFIG)
        curseur = connexion.cursor(dictionary=True)

        curseur.callproc("sp_lire_resultat_nuit", [id_nuit])

        resultat = None
        for jeu_resultat in curseur.stored_results():
            resultat = jeu_resultat.fetchone()

        curseur.close()

    except MySQLError as erreur:
        raise RuntimeError(
            f"Erreur MySQL lors de l'appel à sp_lire_resultat_nuit "
            f"pour id_nuit={id_nuit} : {erreur}"
        ) from erreur

    finally:
        if connexion is not None and connexion.is_connected():
            connexion.close()

    if resultat is None:
        raise ValueError(
            f"Aucun résultat trouvé pour id_nuit={id_nuit}. "
            f"Avez-vous bien appelé ecrire_resultat_nuit() avant ?"
        )

    return resultat


# ============================================================
# 5) LOAD : courbes PNG
# ============================================================
def generer_courbes(df, id_nuit, dossier_sortie):
    """Génère 3 courbes PNG : SpO2, débit nasal, ronflements."""
    os.makedirs(dossier_sortie, exist_ok=True)
    
    temps_min = df["timestamp_sec"] / 60

    def surligner_evenements(ax):
        """Surligne en rouge clair les zones flag_evenement=1."""
        en_evenement = False
        debut = None
        for i, flag in enumerate(df["flag_evenement"]):
            if flag == 1 and not en_evenement:
                en_evenement = True
                debut = temps_min.iloc[i]
            elif flag == 0 and en_evenement:
                en_evenement = False
                ax.axvspan(debut, temps_min.iloc[i], color="red", alpha=0.15)
        if en_evenement:
            ax.axvspan(debut, temps_min.iloc[-1], color="red", alpha=0.15)

    # SpO2
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(temps_min, df["spo2"], color="steelblue", linewidth=1)
    ax.axhline(90, color="orange", linestyle="--", linewidth=1, label="Seuil hypoxie 90%")
    surligner_evenements(ax)
    ax.set_xlabel("Temps (minutes)")
    ax.set_ylabel("SpO2 (%)")
    ax.set_title(f"Saturation en oxygène : Nuit {id_nuit}")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(dossier_sortie, "spo2.png"), dpi=120)
    plt.close(fig)

    # Débit nasal
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(temps_min, df["debit_nasal_pct"], color="seagreen", linewidth=1)
    surligner_evenements(ax)
    ax.set_xlabel("Temps (minutes)")
    ax.set_ylabel("Débit nasal (% du normal)")
    ax.set_title(f"Débit nasal : Nuit {id_nuit}")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(dossier_sortie, "debit_nasal.png"), dpi=120)
    plt.close(fig)

    # Ronflements
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(temps_min, df["ronflements_db"], color="indianred", linewidth=1)
    ax.axhline(70, color="orange", linestyle="--", linewidth=1, label="Seuil ronflement fort 70dB")
    surligner_evenements(ax)
    ax.set_xlabel("Temps (minutes)")
    ax.set_ylabel("Intensité (dB)")
    ax.set_title(f"Ronflements : Nuit {id_nuit}")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(dossier_sortie, "ronflements.png"), dpi=120)
    plt.close(fig)

    print(f"  Courbes générées dans {dossier_sortie}/")

# ============================================================
# 6) LOAD : rapport médical texte
# ============================================================
def generer_rapport_texte(resultat, dossier_sortie):
    """
    Génère le rapport médical texte à partir du résultat complet
    renvoyé par lire_resultat_nuit() (procédure sp_lire_resultat_nuit).
    """
    os.makedirs(dossier_sortie, exist_ok=True)
    chemin_rapport = os.path.join(dossier_sortie, "rapport.txt")

    iah = float(resultat["iah"])
    diagnostic = diagnostic_depuis_iah(iah)

    contenu = f"""
============================================================
  RAPPORT D'ANALYSE POLYSOMNOGRAPHIQUE
  Clinique du Sommeil d'Arles
============================================================

Patient          : {resultat['prenom']} {resultat['nom']}
Nuit d'étude      : #{resultat['id_nuit']}
Date              : {resultat['date_nuit']}
Type d'examen     : {resultat['type_etude']}
Médecin validateur: Dr {resultat['prenom_medecin']} {resultat['nom_medecin']}

------------------------------------------------------------
  RÉSUMÉ DE LA NUIT
------------------------------------------------------------

Index Apnée-Hypopnée (IAH)      : {iah} événements/heure
Sévérité (calculée par la base)  : {resultat['severite_iah']}

SpO2 minimale                    : {resultat['spo2_min']} %
SpO2 moyenne                     : {resultat['spo2_moy']} %
SpO2 médiane                     : {resultat['spo2_mediane']} %
Durée totale d'hypoxie           : {resultat['duree_hypoxie_min']} minutes

Nombre d'apnées                  : {resultat['nb_apnees']}
Nombre d'hypopnées               : {resultat['nb_hypopnees']}
Nombre de RERA                   : {resultat['nb_rera']}
Nombre de micro-éveils estimé    : {resultat['nb_microeveils']}

Durée apnée moyenne              : {resultat['duree_apnee_moy_sec']} secondes
Durée apnée maximale             : {resultat['duree_apnee_max_sec']} secondes

Position dominante                : {resultat['position_dominante']}
Intensité ronflements (max)       : {resultat['decibels_max']} dB
Intensité ronflements (moy)       : {resultat['decibels_moy']} dB
Ronflements forts (>70dB)         : {resultat['nb_ronflements_forts']}

------------------------------------------------------------
  DIAGNOSTIC
------------------------------------------------------------

{diagnostic}

Commentaire médical :
{resultat['commentaire_medical'] or "(aucun commentaire renseigné)"}

------------------------------------------------------------
  COURBES JOINTES
------------------------------------------------------------

  - spo2.png          : Saturation en oxygène au cours de la nuit
  - debit_nasal.png    : Débit nasal au cours de la nuit
  - ronflements.png    : Intensité des ronflements au cours de la nuit

============================================================
  Rapport généré automatiquement par le pipeline ETL.
  Validé le {resultat['date_validation']} par Dr {resultat['nom_medecin']}.
============================================================
"""

    with open(chemin_rapport, "w", encoding="utf-8") as f:
        f.write(contenu)

    print(f"  Rapport généré : {chemin_rapport}")
    return chemin_rapport


# ============================================================
# 7) LOAD : datalake SQLite
# ============================================================
def initialiser_datalake(chemin_db=DATALAKE_PATH):
    """Crée les tables raw_capteur et curated_nuit si elles n'existent pas."""
    connexion = sqlite3.connect(chemin_db)
    connexion.execute("""
        CREATE TABLE IF NOT EXISTS raw_capteur (
            id_raw                INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nuit               INTEGER NOT NULL,
            timestamp_sec         INTEGER NOT NULL,
            spo2                  REAL,
            debit_nasal_pct       REAL,
            effort_thoracique_pct REAL,
            position              TEXT,
            ronflements_db        REAL,
            flag_evenement        INTEGER CHECK (flag_evenement IN (0,1))
        )
    """)
    connexion.execute("""
        CREATE TABLE IF NOT EXISTS curated_nuit (
            id_curated            INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nuit               INTEGER NOT NULL,
            spo2_min              REAL,
            spo2_moy              REAL,
            spo2_mediane          REAL,
            nb_apnees             INTEGER,
            nb_hypopnees          INTEGER,
            nb_rera               INTEGER,
            nb_microeveils        INTEGER,
            duree_hypoxie_min     REAL,
            position_dominante    TEXT,
            decibels_max          REAL,
            decibels_moy          REAL,
            nb_ronflements_forts  INTEGER
        )
    """)
    connexion.commit()
    connexion.close()


def alimenter_raw_capteur(df, id_nuit, chemin_db=DATALAKE_PATH):
    """
    Insère le DataFrame brut dans raw_capteur (datalake).
    pandas sait écrire directement dans SQLite via to_sql().
    """
    connexion = sqlite3.connect(chemin_db)

    df_a_inserer = df.copy()
    df_a_inserer.insert(0, "id_nuit", id_nuit)

    df_a_inserer.to_sql("raw_capteur", connexion, if_exists="append", index=False)

    connexion.close()
    print(f"  {len(df)} lignes insérées dans raw_capteur (datalake)")


def alimenter_curated_nuit(id_nuit, resultat, chemin_db=DATALAKE_PATH):
    """Insère la ligne agrégée dans curated_nuit, depuis le résultat lu en base."""
    connexion = sqlite3.connect(chemin_db)

    df_curated = pd.DataFrame([{
        "id_nuit": id_nuit,
        "spo2_min": float(resultat["spo2_min"]),
        "spo2_moy": float(resultat["spo2_moy"]),
        "spo2_mediane": float(resultat["spo2_mediane"]),
        "nb_apnees": resultat["nb_apnees"],
        "nb_hypopnees": resultat["nb_hypopnees"],
        "nb_rera": resultat["nb_rera"],
        "nb_microeveils": resultat["nb_microeveils"],
        "duree_hypoxie_min": float(resultat["duree_hypoxie_min"]),
        "position_dominante": resultat["position_dominante"],
        "decibels_max": float(resultat["decibels_max"]),
        "decibels_moy": float(resultat["decibels_moy"]),
        "nb_ronflements_forts": resultat["nb_ronflements_forts"],
    }])

    df_curated.to_sql("curated_nuit", connexion, if_exists="append", index=False)

    connexion.close()
    print(f"  Ligne curated_nuit insérée pour id_nuit={id_nuit}")


def deplacer_csv_traite(chemin_csv_source, dossier_traite="raw/traite"):
    """
    Déplace (et non copie) le CSV brut traité vers raw/traite/.

    Important : on utilise shutil.move() et non shutil.copy2().
    Une copie laisserait le fichier original dans raw/, qui serait
    alors retrouvé et retraité au prochain lancement du script
    pour la même nuit. Le déplacement vide raw/ au fur et à mesure,
    qui ne contient ainsi que les CSV pas encore traités.
    """
    os.makedirs(dossier_traite, exist_ok=True)
    destination = os.path.join(dossier_traite, os.path.basename(chemin_csv_source))
    shutil.move(chemin_csv_source, destination)
    print(f"  CSV déplacé : {chemin_csv_source} -> {destination}")


# ============================================================
# ORCHESTRATION : pipeline complet
# ============================================================
def executer_pipeline(id_nuit, id_medecin_validateur):
    """
    Orchestre le pipeline complet pour une nuit donnée.
    Le CSV correspondant est retrouvé automatiquement dans raw/
    grâce à la convention de nommage signal_psg_patient_<id>_nuit_<id_nuit>.csv

    En cas d'erreur à n'importe quelle étape, le message est affiché
    clairement sur stderr puis l'exception est relevée (utile pour
    le débogage et pour qu'un script appelant sache que ça a échoué).
    """
    try:
        chemin_csv, id_patient = trouver_csv_depuis_id_nuit(id_nuit)

        print(f"\n{'='*60}")
        print(f"  TRAITEMENT : Patient #{id_patient} / Nuit #{id_nuit}")
        print(f"  Fichier trouvé : {chemin_csv}")
        print(f"{'='*60}")

        # --- EXTRACT ---
        print("\n[1/6] Extraction du CSV capteur (pandas)...")
        df = lire_csv_capteur(chemin_csv)
        print(f"  {len(df)} lignes lues")

        # --- TRANSFORM ---
        print("\n[2/6] Calcul des indicateurs depuis le signal (pandas)...")
        indicateurs = calculer_indicateurs_signal(df, (df["timestamp_sec"].iloc[-1])/60)
        print(f"  SpO2 min: {indicateurs['spo2_min']} | "
              f"Position dominante: {indicateurs['position_dominante']}")

        # --- LOAD : écriture via procédure ---
        print("\n[3/6] Écriture du résultat via sp_creer_resultat_nuit...")
        confirmation = ecrire_resultat_nuit(id_nuit, id_medecin_validateur, indicateurs)
        print(f"  IAH calculé par la procédure : {confirmation['iah']}")
        print(f"  Diagnostic : {diagnostic_depuis_iah(float(confirmation['iah']))}")

        # --- LOAD : lecture via procédure pour le rapport ---
        print("\n[4/6] Lecture du résultat complet via sp_lire_resultat_nuit...")
        resultat = lire_resultat_nuit(id_nuit)

        # --- LOAD : courbes + rapport ---
        print("\n[5/6] Génération des courbes et du rapport médical...")
        dossier_sortie = f"nuits/{id_nuit}"
        generer_courbes(df, id_nuit, dossier_sortie)
        generer_rapport_texte(resultat, dossier_sortie)

        # --- LOAD : datalake ---
        print("\n[6/6] Alimentation du datalake SQLite...")
        initialiser_datalake()
        alimenter_raw_capteur(df, id_nuit)
        alimenter_curated_nuit(id_nuit, resultat)
        deplacer_csv_traite(chemin_csv)

        print(f"\n✓ Pipeline terminé : Patient #{id_patient} / Nuit #{id_nuit}\n")
        return resultat

    except Exception as erreur:
        print(
            f"\n✗ ERREUR dans le pipeline pour id_nuit={id_nuit} : {erreur}",
            file=sys.stderr
        )
        raise


# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python pipeline_etl_pandas.py <id_nuit> <id_medecin_validateur>")
        print("Exemple : python pipeline_etl_pandas.py 1 2")
        sys.exit(1)

    try:
        id_nuit_arg = int(sys.argv[1])
        id_medecin_validateur_arg = int(sys.argv[2])
    except ValueError:
        print("Erreur : id_nuit et id_medecin_validateur doivent être des nombres entiers.", file=sys.stderr)
        sys.exit(1)

    try:
        executer_pipeline(id_nuit_arg, id_medecin_validateur_arg)
    except Exception as erreur:
        print(f"Erreur fatale : {erreur}", file=sys.stderr)
        sys.exit(1)