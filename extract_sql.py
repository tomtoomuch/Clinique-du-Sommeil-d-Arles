import mysql.connector
from extract_csv import nuit_id, patient_id
from transformation_CSV import df_nuit

nuit_id = int(nuit_id)

cnx = mysql.connector.connect(
    user = 'root',
    password = '4cc3sB4s3D3D*nn33s',
    host = 'localhost',
    database = 'clinique_sommeil',
    port = '3308'
)

cur = cnx.cursor(dictionary=True)
cur.execute("""SELECT resultat_nuit.date_validation, resultat_nuit.iah, resultat_nuit.spo2_min, resultat_nuit.spo2_moy, resultat_nuit.spo2_mediane, resultat_nuit.nb_apnees, resultat_nuit.nb_hypopnees, resultat_nuit.nb_rera, resultat_nuit.nb_microeveils, resultat_nuit.duree_sommeil_min, resultat_nuit.duree_hypoxie_min, resultat_nuit.position_dominante, resultat_nuit.duree_apnee_moy_sec, resultat_nuit.duree_apnee_max_sec, resultat_nuit.decibels_max, resultat_nuit.decibels_moy, resultat_nuit.nb_ronflements_forts, resultat_nuit.severite_iah, resultat_nuit.commentaire_medical, nuit_etude.id_patient, patient.nom
            FROM resultat_nuit 
            LEFT JOIN nuit_etude ON resultat_nuit.id_nuit = nuit_etude.id_nuit
            LEFT JOIN patient ON nuit_etude.id_patient = patient.id_patient
            WHERE resultat_nuit.id_nuit = %s;""", (nuit_id,))
resultat_nuit = cur.fetchall()
#print(resultat_nuit)