import csv
import numpy as np
import matplotlib.pyplot as plt

from extract_csv import df
from ecriture_rapport import url

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