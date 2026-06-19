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

#nb_ronflements_forts = COUNT(ronflements_db > 70) (extrapolé)
nb_ronflements_forts = (df["ronflements_db"] > 70).sum() * 7

#position_dominante = MODE(position)
position_dominante = df["position"].mode()[0]

#Compter le nombre de secondes où spo2 < 90 (extrapolé)
duree_hypoxie_min = (df["spo2"] < 90).sum() * (10 / 60) * 7


resultats = {
    "spo2_min": spo2_min,
    "spo2_moy": spo2_moy,
    "spo2_mediane": spo2_mediane,
    "decibels_max": decibels_max,
    "decibels_moy": decibels_moy,
    "nb_ronflements_forts": nb_ronflements_forts,
    "position_dominante": position_dominante,
    "duree_hypoxie_min": duree_hypoxie_min
}


print("Résultats extrapolés :")
for cle in resultats:
    print(cle, ":", resultats.get(cle))

df_nuit = pd.DataFrame([resultats])
print(df_nuit)