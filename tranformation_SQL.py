import mysql.connector
from extract_csv import nuit_id
from mdp import motdepasse, bdd, port

nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = motdepasse,
    host = 'localhost',
    database = bdd,
    port = port
)

cur = cnx.cursor(dictionary=True)
donnees_sql = cur.execute(nbrapneeProc, parametre)

print(donnees_sql)
