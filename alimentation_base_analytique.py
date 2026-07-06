import os
import sys
import shutil
import sqlite3
import mysql.connector
import pandas as pd
import warnings
from datetime import datetime, timedelta

from mdp import motdepasse, bdd, port

warnings.filterwarnings("ignore", category=UserWarning)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password=motdepasse,
    database=bdd,
    port=port,
)

cur_mysql = conexion.cursor(dictionary=True)
conexion_sqlite = sqlite3.connect("base_analytique.db")
cursor_sqlite = conexion_sqlite.cursor()


# =============================================================
# Alimentation de la table dim_temps dans la base_analytique (SQLit)
# =============================================================

def charger_dim_temps ():
    # Dates de début et de fin
    date_debut = datetime(2020, 1, 1)
    date_fin = datetime(2027, 12, 31)

    # Initialisation
    date_courante = date_debut

    # Jours de la semaine
    jours = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche"
    ]

    while date_courante <= date_fin:

        id_temps = int(date_courante.strftime("%Y%m%d"))
        date_complete = date_courante.strftime("%Y-%m-%d")
        annee = date_courante.year
        mois = date_courante.month
        jour = date_courante.day
        trimestre = (mois - 1) // 3 + 1
        jour_semaine = jours[date_courante.weekday()]
        est_weekend = 1 if date_courante.weekday() >= 5 else 0

        cursor_sqlite.execute(
            "SELECT 1 FROM dim_temps WHERE id_temps = ?",
            (id_temps,)
        )

        if cursor_sqlite.fetchone() is None:
            cursor_sqlite.execute("""
                INSERT INTO dim_temps (
                    id_temps,
                    date_complete,
                    annee,
                    mois,
                    jour,
                    trimestre,
                    jour_semaine,
                    est_weekend
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_temps,
                date_complete,
                annee,
                mois,
                jour,
                trimestre,
                jour_semaine,
                est_weekend
            ))

        date_courante += timedelta(days=1)

    # print("Dimension temps mise à jour.")

# =============================================================
# Alimentation de la table dim_patient dans la base_analytique (SQLit) depuis la base MySQL
# =============================================================

def charger_dim_patient(id_patient):
    query = """
        SELECT
            id_patient, nom, prenom, date_naissance, sexe,
            imc_initial, fumeur AS fumeur_initial,
            pa_tabac AS pa_tabac_initial, profession,
            niveau_activite, CURDATE() AS date_maj
        FROM patient
        WHERE id_patient = %s
    """
    df = pd.read_sql(query, conexion, params= [id_patient])

    if df.empty:
        print(f"Patient {id_patient} introuvable")
        return

    fila = df.iloc[0]
    # print(fila)

    cursor_sqlite.execute(
        """INSERT OR IGNORE INTO dim_patient
           (id_patient, nom, prenom, date_naissance, sexe, imc_initial,
            fumeur_initial, pa_tabac_initial, profession, niveau_activite, date_maj)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
           (
        int(fila["id_patient"]),
        str(fila["nom"]),
        str(fila["prenom"]),
        str(fila["date_naissance"]),
        str(fila["sexe"]),
        float(fila["imc_initial"]),
        str(fila["fumeur_initial"]),
        float(fila["pa_tabac_initial"]),
        str(fila["profession"]),
        str(fila["niveau_activite"]),
        str(fila["date_maj"]),
    )

    )
    conexion_sqlite.commit()
    print(f"Patient {id_patient} traité")


    # charger_dim_patient(id_patient)


# =============================================================
# Alimentation de la table fait_nuit dans la base_analytique (SQLit) depuis la base MySQL
# =============================================================

def charger_fait_nuit(id_patient):

    print([id_patient])
    df = pd.read_sql("call cliniquesommeil2.recuperation_donnees_pour_faits_nuit_base_analytique(%s)", conexion, params=[id_patient])

    if df.empty:
        print(f"Patient {id_patient} introuvable")
    else:

        fila1= df.iloc[id_patient]
        print("pct_apnees_centrales")
        



    cursor_sqlite.execute(
        """INSERT OR IGNORE INTO faits_nuits
            (iah, severite_iah, spo2_min, spo2_moy, spo2_mediane, nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,duree_sommeil_min,
            duree_hypoxie_min, position_dominante, decibels_max, decibels_moy, nb_ronflements_forts, pct_apnees_centrales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            float(fila1["iah"]),
            str(fila1["severite_iah"]),
            float(fila1["spo2_min"]),
            float(fila1["spo2_moy"]),
            float(fila1["spo2_mediane"]),
            int(fila1["nb_apnees"]),
            int(fila1["nb_hypopnees"]),
            int(fila1["nb_rera"]),
            int(fila1["nb_microeveils"]),
            int(fila1["duree_sommeil_min"]),
            float(fila1["duree_hypoxie_min"]),
            str(fila1["position_dominante"]),
            float(fila1["decibels_max"]),
            float(fila1["decibels_moy"]),
            int(fila1["nb_ronflements_forts"]),
            float(fila1["pct_apnees_centrales"]),
        ))
    # charger_fait_nuit(id_patient)  


# ============================================================
# ORCHESTRATION : pipeline complet
# ============================================================
def executer_pipeline(id_patient):
    """
    Orchestre le pipeline complet pour un patient donné.
    
    En cas d'erreur à n'importe quelle étape, le message est affiché
    clairement sur stderr puis l'exception est relevée (utile pour
    le débogage et pour qu'un script appelant sache que ça a échoué).
    """
    try:
       
        # --- Alimenter dim_temps ---
        print("\n[1/3] alimenter_dim_temps")
        charger_dim_temps()
        # print(df)
        # print(f"  {len(df)} dim_temps_mis_a_jour")
       
        # --- Alimenter dim_patient ---
        print("\n[2/3] alimenter_dim_patient")
        print(f"  Alimentation : Patient #{id_patient}")
        charger_dim_patient(id_patient)
    

        # --- Alimenter fait_nuit ---
        print("\n[3/3] alimenter_fait_nuit")
        print(f"  Alimentation : fait_nuit #{id_patient}")
        charger_fait_nuit(id_patient)

        print(f"\n✓ Pipeline terminé : Patient #{id_patient}\n")
       

    except Exception as erreur:
        print(
            f"\n✗ ERREUR dans le pipeline pour id_patient={id_patient} : {erreur}",
            file=sys.stderr
        )
        raise
   

# ============================================================
# POINT D'ENTRÉE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python alimentation_base_analytique.py <id_patient>")
        print("Exemple : alimentation_base_analytique.py 1")
        sys.exit(1)

    try:
        id_patient_arg = int(sys.argv[1])
    except ValueError:
        print("Erreur : id_patient doivent être des nombres entiers.", file=sys.stderr)
        sys.exit(1)
   
    try:
        executer_pipeline(id_patient_arg)
    finally :
        conexion.close()
        conexion_sqlite.close()
    # except Exception as erreur:
    #     print(f"Erreur fatale : {erreur}", file=sys.stderr)
    #     sys.exit(1)

