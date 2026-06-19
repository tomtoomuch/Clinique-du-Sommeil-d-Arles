import csv
import numpy as np
import matplotlib.pyplot as plt

from extract_csv import df

spo2 = df["spo2"]
timestamp_sec = df ["timestamp_sec"]
debit_nasal_pct = df["debit_nasal_pct"]
ronflements_db = df["ronflements_db"]

evolution_saturation = plt.plot(timestamp_sec,spo2)
# affiche la figure à l'écran
plt.show() 

evolution_debit_nasal = plt.plot(timestamp_sec,debit_nasal_pct)

plt.show() 

evolution_ronflements_db = plt.plot(timestamp_sec,ronflements_db)

plt.show() 

 
for i in range(len (spo2))
spo2 + spo2
spo2_minute =

evolution_saturation = plt.plot(timestamp_sec,spo2_minute)
# affiche la figure à l'écran
plt.show() 