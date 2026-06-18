import pandas as pd
import glob
#import os

#patient_id et nuit_id vont etre manipuler par un input
patient_id = "1"
nuit_id = "1"



#BASE_DIR = os.path.dirname(os.path.abspath())
#csv_path = os.path.join(BASE_DIR, "dossier", "moncsv.csv")

csv_patient_1 = glob.glob(f"raw/*{patient_id}*{nuit_id}*.csv")

df = pd.read_csv(csv_patient_1[0], encoding="utf-8-sig")

#exemple pour l'extaction df_patient1["spo2"] => variable["colonne"]
#pour importer les variables dans autres fichiers => from extract_csv import  df_patient1, df_patient2

