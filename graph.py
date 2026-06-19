import csv
import numpy as np
import matplotlib.pyplot as plt

from extract_csv import df

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
plt.show() 

#Graphique évolution du debit nasal
evolution_debit_nasal = plt.plot(timestamp_sec,debit_nasal_pct)
plt.title('Evolution du debit nasal')
plt.xlabel('Temps secondes')
plt.ylabel('Debit nasal en %')
plt.show() 

#Graphique évolution des ronflements
evolution_ronflements_db = plt.plot(timestamp_sec,ronflements_db)
plt.title('Evolution ronflement')
plt.xlabel('Temps secondes')
plt.ylabel('Ronflement en décibel')
plt.show() 

