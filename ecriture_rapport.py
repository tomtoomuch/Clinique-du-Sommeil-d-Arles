from extract_csv import nuit_id, patient_id, df
from extract_sql import resultat_nuit
import matplotlib.pyplot as plt
import os

# On crée le dossier pour stocker le rapport de la nuit
os.mkdir("./nuit/nuit-"+nuit_id+"")
# On stocke le chemin pour l'écriture des fichiers de rapport et de graphiques
url = "./nuit/nuit-"+nuit_id+"/rapport-patient-"+patient_id+"-nuit-"+nuit_id+".txt"
# On écrit le rapport ligne par ligne avec les données du patient
with open(url, "w", encoding="utf-8-sig") as rapport:
    rapport.write(f"Patient {resultat_nuit[0]["severite_iah"]} ({resultat_nuit[0]["nom"]}, nuit {resultat_nuit[0]["nom"]})\n")
    rapport.write(f"IAH : {resultat_nuit[0]["iah"]}/h → diagnostic SAHOS {resultat_nuit[0]["severite_iah"]}\n") 
    rapport.write(f"SpO2 min : {resultat_nuit[0]["spo2_min"]} | moy : {resultat_nuit[0]["spo2_moy"]} | médiane : {resultat_nuit[0]["spo2_mediane"]}\n")
    rapport.write(f"nb_apnees : {resultat_nuit[0]["nb_apnees"]} | nb_hypopnees : {resultat_nuit[0]["nb_hypopnees"]} | nb_rera : {resultat_nuit[0]["nb_rera"]} | nb_microeveils : {resultat_nuit[0]["nb_microeveils"]}\n")
    rapport.write(f"Position dominante : {resultat_nuit[0]["position_dominante"]}\n")
    rapport.write(f"Durée hypoxie : {resultat_nuit[0]["duree_hypoxie_min"]} min\n")
    rapport.write(f"Durée apnée moy : {resultat_nuit[0]["duree_apnee_moy_sec"]} | max : {resultat_nuit[0]["duree_apnee_max_sec"]} s\n")
    rapport.write(f"Décibels max : {resultat_nuit[0]["decibels_max"]} | moy : {resultat_nuit[0]["decibels_moy"]}\n")
    rapport.write(f"Ronflements forts (>70dB) : {resultat_nuit[0]["nb_ronflements_forts"]}\n")
    rapport.write(f"Durée sommeil : {resultat_nuit[0]["duree_sommeil_min"]} min\n")

url_graphs = url.split("/")
url_graphs.pop(-1)
url_graphs = "/".join(url_graphs) + "/"

spo2 = df["spo2"]
timestamp_sec = df ["timestamp_sec"]
debit_nasal_pct = df["debit_nasal_pct"]
ronflements_db = df["ronflements_db"]

#Graphique évolution de la saturation
evolution_saturation = plt.plot(timestamp_sec,spo2)
plt.title('Evolution de la saturation')
plt.xlabel('Temps secondes')
plt.ylabel('SPO2')
# affiche la figure à l'écran
plt.savefig(f"{url_graphs}evolution_saturation.png", transparent=True, dpi=300)
plt.savefig(f"{url_graphs}evolution_saturation.pdf", dpi=300)

#Graphique évolution du debit nasal
evolution_debit_nasal = plt.plot(timestamp_sec,debit_nasal_pct)
plt.title('Evolution du debit nasal')
plt.xlabel('Temps secondes')
plt.ylabel('Debit nasal en %')
plt.savefig(f"{url_graphs}evolution_debit_nasal.png", transparent=True, dpi=300)
plt.savefig(f"{url_graphs}evolution_debit_nasal.pdf", dpi=300)

#Graphique évolution des ronflements
evolution_ronflements_db = plt.plot(timestamp_sec,ronflements_db)
plt.title('Evolution ronflement')
plt.xlabel('Temps secondes')
plt.ylabel('Ronflement en décibel')
plt.savefig(f"{url_graphs}evolution_ronflements_db.png", transparent=True, dpi=300)
plt.savefig(f"{url_graphs}evolution_ronflements_db.pdf", dpi=300)