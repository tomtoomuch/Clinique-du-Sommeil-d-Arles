import os
import sys
import shutil
import sqlite3
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta

from mdp import motdepasse, bdd, port


# =============================================================
# Alimentation de la table dim_temps dans la base_analytique (SQLit)
# =============================================================
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=motdepasse,
        database=bdd,
        port=port,
        use_pure = True
    )
def charger_dim_temps (conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()

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

        conn_sqlite.commit()

# =============================================================
# Alimentation de la table dim_patient dans la base_analytique (SQLit) depuis la base MySQL
# =============================================================

def charger_dim_patient(id_patient, conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()
   
    conexion_mysql = None
    conexion_sqlite = None

    try:
        conexion_mysql = get_mysql_connection()
        cursor_mysql = conexion_mysql.cursor(dictionary=True)

        conexion_sqlite = sqlite3.connect("base_analytique.db")
        cursor_sqlite = conexion_sqlite.cursor()

        query = """
            SELECT
                id_patient, nom, prenom, date_naissance, sexe,
                imc_initial, fumeur AS fumeur_initial,
                pa_tabac AS pa_tabac_initial, profession,
                niveau_activite, CURDATE() AS date_maj
            FROM patient
            WHERE id_patient = %s
        """

        cursor_mysql.execute(query, (id_patient,))
        fila = cursor_mysql.fetchone()

        if fila is None:
            print(f"Patient {id_patient} introuvable")
            return

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

    finally:
        if conexion_mysql is not None and conexion_mysql.is_connected():
            conexion_mysql.close()

        if conexion_sqlite is not None:
            conexion_sqlite.close()

    conn_sqlite.commit()


# =============================================================
# Alimentation de la table fait_nuit dans la base_analytique (SQLit) depuis la base MySQL
# =============================================================

def charger_fait_nuit(id_patient, conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()

    print([id_patient])
    conexion_mysql = get_mysql_connection()

    df = pd.read_sql(
    "call nuitsommeil2.recuperation_donnees_pour_faits_nuit_base_analytique(%s)",
    conexion_mysql,
    params=[id_patient]
)

    if df.empty:
        print(f"Patient {id_patient} introuvable")
    
    else:

        fila1= df.iloc[0]
    
        cursor_sqlite.execute (
        """INSERT OR IGNORE INTO faits_nuits
            (id_nuit,id_patient,id_temps,iah, severite_iah, spo2_min, spo2_moy, spo2_mediane, nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,duree_sommeil_min,
            duree_hypoxie_min, position_dominante, decibels_max, decibels_moy, nb_ronflements_forts, id_suivi_le_plus_proche, pct_apnees_centrales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            int (fila1["id_nuit"]),
            int (fila1["id_patient"]),
            int (fila1["id_temps"]),
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
            int(fila1["id_suivi_le_plus_proche"]),
            float(fila1["pct_apnees_centrales"]),
        )
        )

    conn_sqlite.commit()
    conexion_mysql.close()

# ============================================================
# ORCHESTRATION : pipeline complet
# ============================================================
def executer_pipeline(id_patient):
    print("\n[1/3] alimenter_dim_temps")
    print("\n[2/3] alimenter_dim_patient")
    print("\n[3/3] alimenter_fait_nuit")

    conn_sqlite = sqlite3.connect("base_analytique.db")

    """
    Orchestre le pipeline complet pour un patient donné.
    
    En cas d'erreur à n'importe quelle étape, le message est affiché
    clairement sur stderr puis l'exception est relevée (utile pour
    le débogage et pour qu'un script appelant sache que ça a échoué).
    """
    try:
       
        # --- Alimenter dim_temps ---
        print("\n[1/3] alimenter_dim_temps")
        charger_dim_temps(conn_sqlite)

        
        # --- Alimenter dim_patient ---
        print("\n[2/3] alimenter_dim_patient")
        print(f"  Alimentation : Patient #{id_patient}")
        charger_dim_patient(id_patient, conn_sqlite)
    

        # --- Alimenter fait_nuit ---
        print("\n[3/3] alimenter_fait_nuit")
        print(f"  Alimentation : fait_nuit #{id_patient}")
        charger_fait_nuit(id_patient, conn_sqlite)

        print(f"\n✓ Pipeline terminé : Patient #{id_patient}\n")
       

    except Exception as e:
        conn_sqlite.rollback()
        print(f"✗ ERREUR dans le pipeline pour id_patient={id_patient} : {e}")
        raise

    finally:
        conn_sqlite.close()
   

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
   
    # try:
    #     executer_pipeline(id_patient_arg)
    # finally :
    #     conexion_sqlite.close()
    # # except Exception as erreur:
    # #     print(f"Erreur fatale : {erreur}", file=sys.stderr)
    # #     sys.exit(1)

