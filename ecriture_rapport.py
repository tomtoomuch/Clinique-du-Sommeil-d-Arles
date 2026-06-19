from extract_csv import nuit_id, patient_id
from extract_sql import resultat_nuit
import pandas as pd

url = "./nuit/nuit-"+nuit_id+"/rapport-patient-"+patient_id+"-nuit-"+nuit_id+".txt"

print(url)
with open(url, "w", encoding="utf-8-sig") as rapport:
    rapport.write(f"Patient {resultat_nuit[0]["severite_iah"]} ({resultat_nuit[0]["nom"]}, nuit {resultat_nuit[0]["nom"]})")
    rapport.write(f"IAH : {resultat_nuit[0]["iah"]}/h → diagnostic SAHOS {resultat_nuit[0]["severite_iah"]}") 
    rapport.write(f"SpO2 min : {resultat_nuit[0]["spo2_min"]} | moy : {resultat_nuit[0]["spo2_moy"]} | médiane : {resultat_nuit[0]["spo2_mediane"]}")
    rapport.write(f"nb_apnees : {resultat_nuit[0]["nb_apnees"]} | nb_hypopnees : {resultat_nuit[0]["nb_hypopnees"]} | nb_rera : {resultat_nuit[0]["nb_rera"]} | nb_microeveils : {resultat_nuit[0]["nb_microeveils"]}")
    rapport.write(f"Position dominante : {resultat_nuit[0]["position_dominante"]}")
    rapport.write(f"Durée hypoxie : {resultat_nuit[0]["duree_hypoxie_min"]} min")
    rapport.write(f"Durée apnée moy : {resultat_nuit[0]["duree_apnee_moy_sec"]} | max : {resultat_nuit[0]["duree_apnee_max_sec"]}s")
    rapport.write(f"Décibels max : {resultat_nuit[0]["decidels_max"]} | moy : {resultat_nuit[0]["decibels_moy"]}")
    rapport.write(f"Ronflements forts (>70dB) : {resultat_nuit[0]["nb_ronflements_forts"]}")
    rapport.write(f"Durée sommeil : {resultat_nuit[0]["duree_sommeil_min"]} min")