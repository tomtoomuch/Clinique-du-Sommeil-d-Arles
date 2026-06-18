# Exporter dans SQLite (datalake): archiver les données brutes.
# Aunque mañana cambie MySQL, quiero conservar una copia de los datos originales.
cnx_sqlite = sqlite3.connect("datalake.db")
cursqlite = cnx_sqlite.cursor()

cursqlite.execute("CREATE TABLE IF NOT EXISTS datalakepouls (heure INT, pouls INT)")
cursqlite.execute("CREATE TABLE IF NOT EXISTS datalaketension (heure INT, tension INT)")

for h, p in enumerate(pouls):
    cursqlite.execute("INSERT INTO datalakepouls VALUES (?, ?)", (h, p))

for h, t in enumerate(tensions):
    cursqlite.execute("INSERT INTO datalaketension VALUES (?, ?)", (h, t))

cnx_sqlite.commit()