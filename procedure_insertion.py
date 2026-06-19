import mysql.connector
from extract_csv import nuit_id
from transformation_CSV import df_nuit
from mdp import motdepasse, bdd, port


print(df_nuit)
#nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = motdepasse,
    host = 'localhost',
    database = bdd,
    port = port
)

id_nuit = nuit_id
spo2_min = df_nuit["spo2_min"]
spo2_moy = df_nuit["spo2_moy"]
spo2_mediane = df_nuit["spo2_mediane"]
#duree_sommeil_min = 420
duree_hypoxie_min = df_nuit["duree_hypoxie"]
position_dominante = df_nuit["position_dominante"]
decibels_max = df_nuit["decibels_max"]
decibels_moy = df_nuit["decibels_moy"]
nb_ronflements_forts = df_nuit["nb_ronflements"]

cur = cnx.cursor(dictionary=True)
cur.callproc('insert_data_resultat',(id_nuit, spo2_min, spo2_moy, spo2_mediane, nb_ronflements_forts, decibels_max, decibels_moy, position_dominante, duree_hypoxie_min))
cnx.commit()
