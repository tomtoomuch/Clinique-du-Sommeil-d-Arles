import mysql.connector
from extract_csv import nuit_id

nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = 'Malbosc!2025',
    host = 'localhost',
    database = 'resultatsnuitsommeil',
    port = '3306'
)

cur = cnx.cursor(dictionary=True)
donnees_sql = cur.execute(nbrapneeProc, parametre)

print(donnees_sql)
