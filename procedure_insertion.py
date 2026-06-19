import mysql.connector
from extract_csv import nuit_id
from transformation_CSV import df_nuit


print(df_nuit)
#nbrapneeProc = "EXEC clinique_sommeil.nbrapnee(?)"
parametre = (nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = 'Malbosc!2025',
    host = 'localhost',
    database = 'resultatsnuitsommeil',
    port = '3306',
  )
 


id_nuit = int(nuit_id)
spo2_min = float(df_nuit["spo2_min"].iloc[0])
spo2_moy = float(df_nuit["spo2_moy"].iloc[0])
spo2_mediane = float(df_nuit["spo2_mediane"].iloc[0])
#duree_sommeil_min = 420
duree_hypoxie_min = round(float(df_nuit["duree_hypoxie_min"].iloc[0]))
position_dominante = str(df_nuit["position_dominante"].iloc[0])
decibels_max = float(df_nuit["decibels_max"].iloc[0])
decibels_moy = float(df_nuit["decibels_moy"].iloc[0])
nb_ronflements_forts = int(df_nuit["nb_ronflements_forts"].iloc[0]) 

print(type(spo2_min), spo2_min)
print(type(position_dominante), position_dominante)
print(type(nb_ronflements_forts), nb_ronflements_forts)
 
cur = cnx.cursor(dictionary=True)
cur.callproc('insert_data_resultat',(id_nuit, spo2_min, spo2_moy, spo2_mediane, nb_ronflements_forts,decibels_max, decibels_moy,  position_dominante, duree_hypoxie_min))
cnx.commit()
