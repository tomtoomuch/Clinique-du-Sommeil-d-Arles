# Exporter dans SQLite (datalake): archiver les données brutes.

import sqlite3
from extract_csv import df, nuit_id
from transformation_CSV import resultats

cnx_sqlite = sqlite3.connect("datalake.db")
cursor = cnx_sqlite.cursor()

id_nuit = int(nuit_id)

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
    0,
    0,
    0,
    0,
    resultats["duree_hypoxie_min"],
    resultats["position_dominante"],
    resultats["decibels_max"],
    resultats["decibels_moy"],
    resultats["nb_ronflements_forts"]
))

cnx_sqlite.commit()
cnx_sqlite.close()

print("Datalake SQLite créé et rempli avec succès.")