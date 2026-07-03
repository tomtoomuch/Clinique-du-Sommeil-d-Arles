import sqlite3
import mysql.connector
from datetime import datetime, timedelta

from mdp import motdepasse, bdd, port

cnx_mysql = mysql.connector.connect(
    user='root',
    password=motdepasse,
    host='localhost',
    database=bdd,
    port=port,
)

cur_mysql = cnx_mysql.cursor(dictionary=True)

# Connexion à la base analytique SQLite
conn = sqlite3.connect("base_analytique.db")
cursor = conn.cursor()

# =============================================================
# Alimentation de la table dim_temps dans la base_analytique (SQLit)
# =============================================================

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

    cursor.execute(
        "SELECT 1 FROM dim_temps WHERE id_temps = ?",
        (id_temps,)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
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

conn.commit()
conn.close()

print("Dimension temps mise à jour.")

# =============================================================
# Alimentation de la table fait_nuit dans la base_analytique (SQLit) depuis la base MySQL
# =============================================================

CREATE PROCEDURE `recuperation_donnees_pour_faits_nuit_base_analytique` (
IN p_id_patient INT
)
BEGIN 
 SELECT
 id_patient,
 resultat_nuit.spo2_min, 
 resultat_nuit.spo2_mediane, 
 resultat_nuit.spo2_moy, 
 resultat_nuit.nb_apnees,
 resultat_nuit.nb_hypopnees,
 resultat_nuit.nb_rera,
 resultat_nuit.nb_microeveils,
 resultat_nuit.duree_sommeil_min,
 resultat_nuit.duree_hypoxie_min,
 resultat_nuit.position_dominante, 
 resultat_nuit.decibels_max, 
 resultat_nuit.decibels_moy,  
 resultat_nuit.nb_ronflements_forts,  
 CASE
    WHEN resultat_nuit.nb_apnees = 0 THEN 0
    ELSE (SELECT COUNT(*)
        FROM evenement_respiratoire
        WHERE evenement_respiratoire.id_nuit = resultat_nuit.id_nuit
          AND evenement_respiratoire.type_evenement = 'apnée centrale'
    )* 100.0 / resultat_nuit.nb_apnees
    END AS ptc_apnees_centrales 

FROM resultat_nuit
LEFT JOIN nuit_etude
    ON resultat_nuit.id_nuit = nuit_etude.id_nuit
WHERE p_id_patient;

END