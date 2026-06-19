import sqlite3
import mysql.connector

from extract_csv import df, nuit_id
from transformation_CSV import resultats

#Variables convertidas de diccionario pandas a solo variable 
id_nuit = int(nuit_id)

spo2_min = float(resultats["spo2_min"])
spo2_moy = float(resultats["spo2_moy"])
spo2_mediane = float(resultats["spo2_mediane"])

duree_hypoxie_min = float(resultats["duree_hypoxie_min"])

position_dominante = str(resultats["position_dominante"])

decibels_max = float(resultats["decibels_max"])
decibels_moy = float(resultats["decibels_moy"])

nb_ronflements_forts = int(resultats["nb_ronflements_forts"])

#conecto mysql

cnx_mysql = mysql.connector.connect(
    user="root",
    password="Malbosc!2025",
    host="localhost",
    database="resultatsnuitsommeil",
    port=3306,
    use_pure=True
)

cur_mysql = cnx_mysql.cursor(dictionary=True)

cur_mysql.execute("""
SELECT
    nb_apnees,
    nb_hypopnees,
    nb_rera
FROM resultat_nuit
WHERE id_nuit = %s
""", (id_nuit,))

ligne_mysql = cur_mysql.fetchone()

nb_apnees = int(ligne_mysql["nb_apnees"])
nb_hypopnees = int(ligne_mysql["nb_hypopnees"])
nb_rera = int(ligne_mysql["nb_rera"])

# calcule
nb_microeveils = nb_apnees + nb_hypopnees + nb_rera

cur_mysql.close()
cnx_mysql.close()

#conection SQL

cnx_sqlite = sqlite3.connect("datalake.db")
cursor = cnx_sqlite.cursor()

#tabla raw

cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_capteur (
    id_raw INTEGER PRIMARY KEY AUTOINCREMENT,
    id_nuit INTEGER NOT NULL,
    timestamp_sec INTEGER NOT NULL,
    spo2 REAL,
    debit_nasal_pct REAL,
    effort_thoracique_pct REAL,
    position TEXT,
    ronflements_db REAL,
    flag_evenement INTEGER CHECK (flag_evenement IN (0,1))
)
""")

#Tabla curada 
cursor.execute("""
CREATE TABLE IF NOT EXISTS curated_nuit (
    id_curated INTEGER PRIMARY KEY AUTOINCREMENT,
    id_nuit INTEGER NOT NULL,
    spo2_min REAL,
    spo2_moy REAL,
    spo2_mediane REAL,
    nb_apnees INTEGER,
    nb_hypopnees INTEGER,
    nb_rera INTEGER,
    nb_microeveils INTEGER,
    duree_hypoxie_min REAL,
    position_dominante TEXT,
    decibels_max REAL,
    decibels_moy REAL,
    nb_ronflements_forts INTEGER
)
""")

#llenado de raw

for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO raw_capteur (
        id_nuit,
        timestamp_sec,
        spo2,
        debit_nasal_pct,
        effort_thoracique_pct,
        position,
        ronflements_db,
        flag_evenement
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_nuit,
        int(row["timestamp_sec"]),
        float(row["spo2"]),
        float(row["debit_nasal_pct"]),
        float(row["effort_thoracique_pct"]),
        str(row["position"]),
        float(row["ronflements_db"]),
        int(row["flag_evenement"])
    ))

#llenado de curate

cursor.execute("""
INSERT INTO curated_nuit (
    id_nuit,
    spo2_min,
    spo2_moy,
    spo2_mediane,
    nb_apnees,
    nb_hypopnees,
    nb_rera,
    nb_microeveils,
    duree_hypoxie_min,
    position_dominante,
    decibels_max,
    decibels_moy,
    nb_ronflements_forts
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    id_nuit,
    spo2_min,
    spo2_moy,
    spo2_mediane,
    nb_apnees,
    nb_hypopnees,
    nb_rera,
    nb_microeveils,
    duree_hypoxie_min,
    position_dominante,
    decibels_max,
    decibels_moy,
    nb_ronflements_forts
))


cnx_sqlite.commit()
cnx_sqlite.close()

print("Datalake SQLite créé et rempli avec succès.")