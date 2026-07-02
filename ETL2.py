import os
import sys
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
    "port": port,
    
}

# DATALAKE_PATH = "datalake.db"
DB_PATH = "base_analytique.db"

# ============================================================
# UTILITAIRE : retrouver le CSV depuis l'id_nuit
# ============================================================
DOSSIER_RAW = "raw"

def trouver_csv_depuis_id_patient(id_patient, dossier_raw=DOSSIER_RAW):
    """
    Retrouve le chemin du CSV à partir du seul id_patient.

    Convention de nommage attendue :
        suivi_cpap_patient_<id_patient>.csv
    Exemple : suivi_cpap_patient_1.csv -> id_patient=1

    Retourne
    --------
    (chemin_complet, id_patient)
    """
    suffixe_recherche = f"_patient_{id_patient}.csv"

    fichiers_trouves = [
        f for f in os.listdir(dossier_raw)
        if f.endswith(suffixe_recherche)
    ]

    if not fichiers_trouves:
        raise FileNotFoundError(
            f"Aucun fichier CSV trouvé pour id_patient={id_patient} "
            f"dans le dossier '{dossier_raw}/'. "
            f"Format attendu : suivi_cpap_patient_{id_patient}.csv"
        )

    if len(fichiers_trouves) > 1:
        raise ValueError(
            f"Plusieurs fichiers correspondent à id_patient={id_patient} : "
            f"{fichiers_trouves}. Vérifiez qu'il n'y a pas de doublon."
        )

    nom_fichier = fichiers_trouves[0]
    chemin_complet = os.path.join(dossier_raw, nom_fichier)


# ============================================================
# 1) EXTRACT : lecture du CSV avec pandas
# ============================================================
def lire_csv_capteur(chemin_fichier):
    """
    Lit le CSV capteur avec pandas et retourne un DataFrame.

    Colonnes attendues :
        id_suivi, id_appareil, date_jour, duree_utilisation_h, iah_residuel,
          fuites_l_min, nb_evenements, qualité donnee

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
        "id_suivi", "id_appareil", "date_jour", "duree_utilisation_h", "iah_residuel",
          "fuites_l_min", "nb_evenements", "qualité_donnee"
        
    }
    colonnes_manquantes = colonnes_obligatoires - set(df.columns)
    if colonnes_manquantes:
        raise ValueError(
            f"Colonnes manquantes dans {chemin_fichier} : {colonnes_manquantes}"
        )

    return df

# ============================================================
# 2) TRANSFORM : calcul des alertes avec pandas
# ============================================================
def calculer_alerte_observance(duree_utilisation_h):
    """
   
    Paramètres
    ----------
    df : DataFrame : sortie de lire_csv_capteur()

    Retourne
    --------
    dict avec les indicateurs prêts à être passés à la procédure.
    """

    if duree_utilisation_h >= 4:
        return 0
    else :
        return 1

 

def calculer_alerte_iah_residuel(iah_residuel):
    """Retourne alerte selon l'IAH_residuel."""
    if iah_residuel >= 5:
        return 1
    else:
        return 0


# ============================================================
# 3) LOAD : base analytique SQLite
# ============================================================
def initialiser_database(chemin_db=DB_PATH):
    """Crée la table faits_suivi_cpap_jour si elle n'existe pas."""
    connexion = sqlite3.connect(chemin_db)
    connexion.execute("""
        CREATE TABLE faits_suivi_cpap_jour (
    id_fait_suivi_jour  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_suivi_source      INTEGER NOT NULL,   -- id_suivi d'origine dans clinique_v2 (traçabilité)
    id_patient           INTEGER NOT NULL,
    id_temps             INTEGER NOT NULL,

    duree_utilisation_h  REAL,
    iah_residuel          REAL,
    fuites_l_min          REAL,
    nb_evenements         INTEGER,
    qualite_donnee        TEXT,

    -- Contexte patient : FK vers le dernier suivi connu à cette date
    -- (même dimension partagée que faits_nuits -- permet de croiser
    -- ex: dérive de l'IAH résiduel avec l'évolution du poids)
    id_suivi_le_plus_proche INTEGER,

    -- Alertes calculées au moment de l'ETL2 (seuils cliniques standards)
    alerte_observance_insuffisante INTEGER NOT NULL DEFAULT 0,  -- 1 si duree < 4h
    alerte_iah_eleve                INTEGER NOT NULL DEFAULT 0,  -- 1 si iah_residuel > 5

    FOREIGN KEY (id_patient) REFERENCES dim_patient(id_patient),
    FOREIGN KEY (id_temps)   REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_suivi_le_plus_proche) REFERENCES dim_suivi_patient(id_suivi)
    )
    """)
    
    connexion.commit()
    connexion.close()





def alimenter_faits_suivi_cpap_jour(id_nuit, resultat, chemin_db=DB_PATH):
   # Prévoir d'alimenter également la base MySQL
    connexion = sqlite3.connect(chemin_db)

    df_cpap = pd.DataFrame([{
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

    df_cpap.to_sql("curated_nuit", connexion, if_exists="append", index=False)

    connexion.close()
    print(f"  Ligne curated_nuit insérée pour id_nuit={id_nuit}")



# ============================================================
# ORCHESTRATION : pipeline complet
# ============================================================
def executer_pipeline(id_patient):
    """
    Orchestre le pipeline complet .
    Le CSV correspondant est retrouvé automatiquement dans raw/
    grâce à la convention de nommage 

    En cas d'erreur à n'importe quelle étape, le message est affiché
    clairement sur stderr puis l'exception est relevée (utile pour
    le débogage et pour qu'un script appelant sache que ça a échoué).
    """
    try:
        chemin_csv = trouver_csv_depuis_id_patient(id_patient)

        print(f"  TRAITEMENT : Patient #{id_patient}")
        print(f"  Fichier trouvé : {chemin_csv}")
        print(f"{'='*60}")

        # --- EXTRACT ---
        print("\n[1/6] Extraction du CSV (pandas)...")
        df = lire_csv_capteur(chemin_csv)
        print(f"  {len(df)} lignes lues")
        
        # --- TRANSFORM ---
        print("\n[2/6] Calcul des alertes depuis le signal (pandas)...")
        indicateurs = calculer_indicateurs_signal(df, (df["timestamp_sec"].iloc[-1])/60)
        print(f"  SpO2 min: {indicateurs['spo2_min']} | "
              f"Position dominante: {indicateurs['position_dominante']}")
        print(['position dominante'])
        # --- LOAD : écriture via procédure ---
        print("\n[3/6] Écriture du résultat via sp_creer_resultat_nuit...")
        confirmation = ecrire_resultat_nuit(id_nuit, id_medecin_validateur, indicateurs, commentaire_medical)
        print(f"  IAH calculé par la procédure : {confirmation['iah']}")
        print(f"  Diagnostic : {diagnostic_depuis_iah(float(confirmation['iah']))}")

        # --- LOAD : lecture via procédure pour le rapport ---
        print("\n[4/6] Lecture du résultat complet via sp_lire_resultat_nuit...")
        resultat = lire_resultat_nuit(id_nuit)

            

        # --- LOAD : datalake ---
        print("\n[6/6] Alimentation de la DB SQLite...")
        initialiser_database()
        alimenter_raw_capteur(df, id_patient)
        alimenter_curated_nuit(id_patient, resultat)
        

        print(f"\n Pipeline terminé : Patient #{id_patient}\n")
        return resultat

    except Exception as erreur:
        print(
            f"\n ERREUR dans le pipeline pour id_patient={id_patient} : {erreur}",
            file=sys.stderr
        )
        raise


# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python ETL2.py <id_patient>")
        print("Exemple : python ETL2.py 1 ")
        sys.exit(1)

    try:
        id_patient_arg = int(sys.argv[1])
        
    except ValueError:
        print("Erreur : id_patient doit être un nombre entier", file=sys.stderr)
        sys.exit(1)

    try:
        executer_pipeline(id_patient_arg)
    except Exception as erreur:
        print(f"Erreur fatale : {erreur}", file=sys.stderr)
        sys.exit(1)

