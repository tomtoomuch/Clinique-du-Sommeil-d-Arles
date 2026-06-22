from extract_csv import patient_id, nuit_id
from transformation_CSV import df_nuit

import pandas as pd

df_nuit.to_csv(f"./raw/traite/signal-psg-patient-{patient_id}-nuit-{nuit_id}-traite.csv", sep=",", index=False, encoding="utf-8-sig")