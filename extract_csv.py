import pandas as pd


df_patient1 = pd.read_csv("signal-psg-patient-1-nuit-1.csv", encoding="utf-8-sig")

df_patient2 = pd.read_csv("signal-psg-patient-2-nuit-2.csv", encoding="utf-8-sig")

#exemple pour l'extaction df_patient1["spo2"] => variable["colonne"]
#pour importer les variables dans autres fichiers => from extract_csv import  df_patient1, df_patient2