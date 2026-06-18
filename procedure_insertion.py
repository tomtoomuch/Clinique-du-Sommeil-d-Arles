import mysql.connector
from extract_csv import nuit_id
from transformation_CSV import df_nuit

#nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = '4cc3sB4s3D3D*nn33s',
    host = 'localhost',
    database = 'clinique_sommeil',
    port = '3308'
)

id_nuit = nuit_id
spo2_min = df_nuit[spo2_min]
spo2_moy = 91.4383
spo2_mediane = 94.45
#duree_sommeil_min = 420
duree_hypoxie_min = 910
position_dominante = "dorsale"
decibels_max = 79.0
decibels_moy = 61.78
nb_ronflements_forts = 749

cur = cnx.cursor(dictionary=True)
cur.callproc('insert_data_resultat',(id_nuit, spo2_min, spo2_moy, spo2_mediane, nb_ronflements_forts, decibels_max, decibels_moy, position_dominante, duree_hypoxie_min))
cnx.commit()
