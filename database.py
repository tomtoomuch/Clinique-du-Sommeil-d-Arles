import sqlite3
import mysql.connector  
from extract_csv import df, nuit_id
from transformation_CSV import resultats

id_nuit = int(nuit_id)

#contecto con mi SQL 
cnx_mysql = mysql.connector.connect(
    user="root",
    password="Malbosc!2025",
    host="localhost",
    database="resultatsnuitsommeil",
    port=3306
)

#esa fila se transforma en un diccionario:
cur_mysql = cnx_mysql.cursor(dictionary=True)

cur_mysql.execute("""
SELECT
    nb_apnees,
    nb_hypopnees,
    nb_rera,
    FROM resultat_nuit
WHERE id_nuit = %s
""", (id_nuit,))

#Dame la primera fila del resultado de la consulta
ligne_mysql = cur_mysql.fetchone()

nb_apnees = ligne_mysql["nb_apnees"]
nb_hypopnees = ligne_mysql["nb_hypopnees"]
nb_rera = ligne_mysql["nb_rera"]
# microéveils = nombre total d'événements
nb_microeveils = nb_apnees + nb_hypopnees + nb_rera

cur_mysql.close()
cnx_mysql.close()


#Conecto a sqlite
cnx_sqlite = sqlite3.connect("datalake.db")
cursor = cnx_sqlite.cursor()

#primera tabla Raw
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

#segunda tabla Tabla curada
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
        row["timestamp_sec"],
        row["spo2"],
        row["debit_nasal_pct"],
        row["effort_thoracique_pct"],
        row["position"],
        row["ronflements_db"],
        row["flag_evenement"]
    ))

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
    resultats["spo2_min"],
    resultats["spo2_moy"],
    resultats["spo2_mediane"],
    nb_apnees,
    nb_hypopnees,
    nb_rera,
    nb_microeveils,
    resultats["duree_hypoxie_min"],
    resultats["position_dominante"],
    resultats["decibels_max"],
    resultats["decibels_moy"],
    resultats["nb_ronflements_forts"]
))

cnx_sqlite.commit()
cnx_sqlite.close()

print("Datalake SQLite créé et rempli avec succès.")