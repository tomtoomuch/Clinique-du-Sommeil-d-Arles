import streamlit as st
import pandas as pd
import numpy as np

import os
import sys
import subprocess
import shutil
import sqlite3
import mysql.connector
from mysql.connector import Error as MySQLError
from datetime import date
from mdp import motdepasse, bdd, port

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": motdepasse,
    "database": bdd,
    "port": port
}

DATALAKE_PATH = "datalake.db"

connexion = mysql.connector.connect(**MYSQL_CONFIG)

st.title("Opérations de saisie d'une nuit d'étude pour diagnostic")
st.subheader("Nuits à traiter")
st.badge(f"Mis à jour le {date.today()}", color="green")

curseur = connexion.cursor(dictionary=True)
curseur.execute("SELECT * FROM nuit_disponible;")
nuits_disponibles = curseur.fetchall()
curseur.close()
menu_options_select_nuit = []
if nuits_disponibles:
    for nuit in nuits_disponibles:
        menu_options_select_nuit.append(f"Nuit {nuit['id_nuit']}")

nuit_selectionnee = st.selectbox(
    "Sélectionner une nuit à ajouter à la base de données et produire le rapport médical pour le médecin",
    (menu_options_select_nuit)   
)
try:
    nuit_selectionnee
    id_nuit = nuit_selectionnee.split(" ").pop(-1)
except NameError:
    print('Aucune nuit disponible')

st.subheader("Médecin validateur")
curseur = connexion.cursor(dictionary=True)
curseur.execute("SELECT * FROM medecinvalidateur;")
medecinsvalidateurs = curseur.fetchall()
curseur.close()
menu_options_select_medecin = []

for medecin in medecinsvalidateurs:
    menu_options_select_medecin.append(f"Dr {medecin['prenom']} {medecin['nom']} - {medecin['specialite']} - ID : {medecin['id_personnel']}")

medecin_validateur = st.selectbox(
    "Sélectionner un médecin qui validera les résultats de la nuit et le rapport médical",
    (menu_options_select_medecin)   
)
#print(medecin_validateur)
medecin_validateur = medecin_validateur.split(" ").pop(-1)

st.subheader("Commentaire à ajouter dans les résultats de la nuit")
commentaire_medical = st.text_area(label="Commentaire du superviseur", value="")

if st.button(label="Lancer l'ETL"):

    #print(nuit_selectionnee)
    #print(medecin_validateur)
    #print(commentaire_superviseur)
    #st.write(f"Le médecin validateur est le Dr {medecin_validateur} pour la nuit {id_nuit}")
    #subprocess.run([sys.executable, f"./pipeline_etl_pandas.py {id_nuit} {medecin_validateur}"])
    python_path = sys.executable
    script_path = f"pipeline_etl_pandas.py {id_nuit} {medecin_validateur} {commentaire_medical}"
    args = [python_path, script_path, "--verbose"]
    try:
        os.execv(python_path, args)
    except OSError as e:
        print(f"Failed to execute script: {e}")
    sys.exit(1)