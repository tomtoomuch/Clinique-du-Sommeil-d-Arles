import pandas as pd
from extract_csv import df

# spo2_min = MIN(spo2)
spo2_min = df["spo2"].min() 

# spo2_moy = AVG(spo2)
spo2_moy = df["spo2"].mean() 

# spo2_mediane = MEDIAN(spo2)
spo2_mediane = df["spo2"].median() 

# decibels_max = MAX(ronflements_db)
decibels_max = df["ronflements_db"].max() 

# decibels_moy = AVG(ronflements_db)
decibels_moy = df["ronflements_db"].mean() 

#nb_ronflements_forts = COUNT(ronflements_db > 70)
nb_ronflements_forts = (df["ronflements_db"] > 70).sum()

#position_dominante = MODE(position)
position_dominante = df["position"].mode()[0]

#Compter le nombre de secondes où spo2 < 90
duree_hypoxie = (df["spo2"] < 90).sum() * 10


resultats = {
    "spo2_min": df["spo2"].min(),
    "spo2_moy": df["spo2"].mean(),
    "spo2_mediane": df["spo2"].median(),
    "decibels_max": df["ronflements_db"].max(),
    "decibels_moy": df["ronflements_db"].mean(),
    "nb_ronflements": ((df["ronflements_db"] > 70).sum()) * 7,
    "position_dominante": df["position"].mode(),
    "duree_hypoxie": (df["spo2"] < 90).sum() * (10/60) * 7
}

# Extrapolation des valeurs pertinentes : nb_ronflements_forts, position_dominante, duree_hypoxemie
resultats.update([("nb_ronflements", nb_ronflements_forts * 7), ("position_dominante", position_dominante), ("duree_hypoxie", duree_hypoxie)])

#print("Résultats extrapolés :")
#for cle in resultats:
#    print(cle, ":", resultats.get(cle))


df_nuit = pd.DataFrame([resultats])
#print(df_nuit)