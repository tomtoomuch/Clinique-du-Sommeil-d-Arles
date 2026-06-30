import streamlit as st
import pandas as pd
import numpy as np

import os
import sys
import shutil
import sqlite3
import mysql.connector
from mysql.connector import Error as MySQLError
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
st.header("Nuits à traiter")
st.badge("Mis à jour le", color="green")

curseur = connexion.cursor(dictionary=True)
curseur.execute("SELECT * FROM nuit_disponible;")
nuits_disponibles = curseur.fetchall()
curseur.close()
menu_options_select_nuit = []

for nuit in nuits_disponibles:
    menu_options_select_nuit.append(f"Nuit {nuit['id_nuit']}")    

nuit_selectionnee = st.selectbox(
    "Sélectionner une nuit à ajouter à la base de données et produire le rapport médical pour le médecin",
    (menu_options_select_nuit)   
)

st.header("Médecin validateur")
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

st.header("Commentaire à ajouter dans les résultats de la nuit")
commentaire_superviseur = st.text_area(label="Commentaire du superviseur", value="")

if st.button(label="Lancer l'ETL"):
    print(nuit_selectionnee)
    print(medecin_validateur)
    print(commentaire_superviseur)
    st.write(f"Le médecin validateur est le Dr {medecin_validateur["nom"]} pour la nuit {nuit_selectionnee}")

