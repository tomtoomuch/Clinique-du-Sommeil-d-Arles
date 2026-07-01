# Clinique-du-Sommeil-d-Arles-Pipeline-ETL-sur-nuit-d-tude
## Le projet
La Clinique du sommeil d'Arles, travaille sur les maladies du sommeil.
Dans ce cadre ils vont passer par une étape de diagnostic du patient et dans un second temps le suivre pendant le traitement.
Lors de la nuit d'étude qui sert au diagnostic ils disposent de deux sources de données pour une nuit d’étude :

- CSV capteur 
- et base de donnée SQL


Ils ont besoins de regrouper les données pour pouvoir permettre au médecin d'avoir une vue d'ensemble pour faire le diagnostic.

Par la suite un infirmier superviseur rentre un commentaire sur les résultats de la nuit via une application.

Enfin le médecin validateur récupère les résultats du patient et les valides via une application.

Toutes les données récupérées et traitées sont utiliser dans une base analytique pour entrainer une IA afin de faciliter les futurs diagnostiques. 

## Les objectifs
- Lire les CSV 
- Calculer les indicateurs cliniques
- Remplir la table resultatnuit avec les indicateurs cliniques du csv et de la table evenementrespiratoire
- Envoiyer le CSV dans le datalake pour usage futur (modèle en étoile faits_nuits)
- Produire un rapport médical avec diagnostic et courbes que le médecin pourra charger plus tard.
- Créer une interface pour l'opérateur (infirmier superviseur)
- Créer une interface pour le médecin validateur
- Alimenter une base de donnée analytique
- Entrainer une IA pour faciliter les futurs diagnostiques

## L'installation

Création d'un environnement Git
```bash
Création d'un répo distant Git
```
Installer SQLite :
Ensuite, vous devez installer la bibliothèque sqlite3, qui vous permettra de manipuler des bases de données SQLite:
```bash
npm install sqlite3
```

Installer Pandas :
Il vous faut ensuite installer Pandas pour la lecture et le traitement des données CSV :
```bash
npm install pandas
```
Installer MySQL :
Ensuite, vous devez installer MySQL pour pouvoir donnercter la base SQL et le script python:
```bash
npm pip install mysql-connector-python
```
Installer Matplotlib :
Ensuite, vous devez installer Matplotlib pour pouvoir réaliser les graphiques des résultats de la nuit d'étude:
```bash
npm pip install matplotlib
```
Installer Glob :
Ensuite, vous devez installer Glob afin de pouvoir relier un fichier à des documents qui sont sur une machine.
```bash
npm pip install glob2
```

Installer Express :
Il vous faut ensuite installer Express pour permettre la création d'API via JS :
```bash
npm install express
```

Installer Streamlit :
```bash 
pip install streamlit 
```

Installer Joblib:
```bash 
pip install joblib
```

Installer Sklearn:
```bash 
pip install -U scikit-learn
```

Installer PDF:
```bash 
pip install fpdf
```

Installer seaborn:
```bash 
pip install seaborn
```

## Extraction et transformation des CSV

Lire le CSV capteur depuis un répertoire raw/

Lire les événements depuis la table evenement_respiratoire (via SQL)

Depuis le CSV :
```bash
spo2_min = MIN(spo2)

spo2_moy = AVG(spo2)

spo2_mediane = MEDIAN(spo2)

decibelsmax = MAX(ronflementsdb)

decibelsmoy = AVG(ronflementsdb)

nbronflementsforts = COUNT(ronflements_db > 70)

position_dominante = MODE(position)

Compter le nombre de secondes où spo2 < 90
```
Depuis evenement_respiratoire :
```bash
nbapnees = COUNT(typeevenement IN ('apnée obstructive','apnée centrale'))

nbhypopnees = COUNT(typeevenement = 'hypopnée')

nbrera = COUNT(typeevenement = 'RERA')

Nombre total d’événements
```
Extrapolation sur la nuit complète :
Les données couvrent 1h de CSV et 2h d’événements, la nuit dure 7h.
```bash
Durée de sommeil : dureesommeilmin ≈ 7h × 60 = 420 min (ou valeur fournie dans les notes techniques)
```
Une fois les calculs réalisés
```bash
Copier le CSV brut dans /raw/traite/
```
Les fichiers crées pour réaliser ces étapes sont :
```bash
- extract_csv.py
- graph.py
- ecriture_csv.py
- transformation_CSV.py
```

## Traitement et alimentation de la bdd

Dans la bdd (avec MySQL Worbench), il faudra remplir la table resultat_nuit avec les informations présente d'une part dans la bdd et d'autre part avec les données des csv. Pour se faire on va :

### Créer deux fichiers qui ne seront pas suivit dans le git pour protéger les accès à la bdd :
mdp.py
```bash
motdepasse = "votremotdepasse"
bdd = "votrenomdebdd"
port = numéro de port que vous utilisez
export =(motdepasse,bdd,port)
```
mdp.js
```bash
const = motDePasse = "votremotdepasse"
const = bdd = "votrenomdebdd"
const = port = numéro de port que vous utilisez
module.exports = {motDePasse, bdd, port}
```
Créer un lien entre MySQL et nos fichiers Python ou JS qui ont besoin d'être connecté :
```bash
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": motdepasse,
    "database": bdd,
    "port": port,
}
```
### Une fois que les fichiers sont connecté, mettre à jour la bdd.

Consulter le fichier **Elements_bdd**. Inserer dans votre bdd toutes les procédures et vu qui sont dans ce fichier.

Dans un second temps il faudra appeler la procedure ci-dessous dans python pour pouvoir y intégrer les données récupérées en CSV, et alimenter la table **resultat_nuit** dans la bdd.
```bash
sp_creer_resultat_nuit
```
Les fichiers crées pour réaliser ces étapes sont :
```bash
- pipeline_etl_pandas.py
- Elements_bdd.db (car la bdd n'est pas suivit par Git)
```
## Générer un rapport pour le médecin

Utilisation d'un Pipeline **app_resultats_nuit_avec_ia**, pour permettre au médecin validateur de récupérer les résultats nuits d'un patient, de faire un commentaire et le valider.

Création d'un espace sur le front pour le commentaire du médecin : 
```bash
st.text("Commentaire validation médical")
            commentaire= st.text_area("")
```
Création d'un **dossier patient** dans lequel sera rangé les résultats des patients:
```bash
folder = Path("patient")
        folder.mkdir(exist_ok=True)
```
Création du bouton **valider**, qui est conditionné au remplissage du commentaire du médecin
```bash
st.header('Valider le rapport')
button1 = st.button('Valider')

if button1: 
    if commentaire != "":
        pdf = FPDF('P', 'mm', 'A4')
    else:  
        st.warning("Renseigner commentaire")
```
Création du PDF **"rapport_valide_patient{ID}"**, dans lequel sera combiné le rapport.txt, les graphs et le commentaire du médecin validateur:
```bash
    #première page : rapport de la nuit
        pdf.add_page()
        pdf.set_font(family='Times', size=12)
        pdf.set_font("helvetica", size=14)
        pdf.multi_cell(0, 8, texte)
        pdf.cell(40, 10, "COMMENTAIRE VALIDATION MEDICAL", ln=True)
        pdf.multi_cell(0, 8, commentaire)
    #seconde page : graph SPO2
        pdf.add_page()
        pdf.image(str(nuit_dir / "spo2.png"), x=10, y=20, w=180)
    #troisième page : graph debit_nasal
        pdf.add_page()
        pdf.image(str(nuit_dir / "debit_nasal.png"), x=10, y=20, w=180)
    #quatrième page : graph ronflement
        pdf.add_page()
        pdf.image(str(nuit_dir / "ronflements.png"), x=10, y=20, w=180)
```
Création du bouton **télécharger**, qui permet au médecin de télécharger le pdf.
```bash
st.download_button(
        "Télécharger PDF",
        data=pdf_bytes,
        file_name = f"rapport_valide_patient_{selected_patient_id}.pdf", 
        mime="application/pdf"
        )
```
## Création d'un datalake pour entrainer une IA

Pour créer le datalake :
Création du fichier database.py


## Création d'une route API pour permettre des connexions sécuriser avec des accés spécifique à la Bdd.


