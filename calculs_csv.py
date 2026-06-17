import mysql.connector
import pandas as pd

donnees_nuit_sql = []
cnx = mysql.connector.connect(
    host="localhost",
    userr="root",
    password="4cc3sB4s3D3D*nn33s",
    database="cliniquesommeil"
)
cur = cnx.cursor(dictionnary=True)
cur.execute("SELECT * FROM evenement_respiratoire WHERE id_nuit = 1")
donnees_nuit_sql = [row for row in cur.fetchall()]
print(donnees_nuit_sql)

donnees_nuit_csv = []
df = pd.read_csv('./raw/signal-psg-patient-1-nuit-1.csv', encoding="utf-8-sig", sep=",")
for row in df:
    for col in row:
        print(col)
    donnees_nuit_csv.append(row)

print(donnees_nuit_csv)



"raw/*" + id_patient + ""