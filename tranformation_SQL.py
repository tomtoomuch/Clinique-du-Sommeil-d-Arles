import mysql.connector
from extract_csv import nuit_id

nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = '4cc3sB4s3D3D*nn33s',
    host = 'localhost',
    database = 'clinique_sommeil',
    port = '3308'
)

cur = cnx.cursor(dictionary=True)
donnees_sql = cur.execute(nbrapneeProc, parametre)

print(donnees_sql)
