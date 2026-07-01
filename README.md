# Clinique-du-Sommeil-d-Arles-Pipeline-ETL-sur-nuit-d-tude
# Le projet
La Clinique du sommeil d'Arles, travaille sur les maladies du sommeil.
Dans ce cadre ils vont passer par une étape de diagnostic du patient et dans un second temps le suivre pendant le traitement.
Lors de la nuit d'étude qui sert au diagnostic ils disposent de deux sources de données pour une nuit d’étude :

CSV capteur (signal brut sur 1h, 1 ligne / 10 secondes)
La table SQL evenement_respiratoire (événements respiratoires déjà détectés et validés sur 2h).

Ils ont besoins de regrouper les données pour pouvoir permettre au médecin d'avoir une vue d'ensemble pour faire le diagnostic.

# L'objectif
- Lire le CSV capteur
- Calculer les indicateurs cliniques
- Remplir la table resultatnuit avec les indicateurs cliniques du csv et de la table evenementrespiratoire
- Envoiyer le CSV dans le datalake pour usage futur (modèle en étoile faits_nuits)
- Produire un rapport médical avec diagnostic et courbes que le médecin pourra charger plus tard.

# L'installation

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

# Extraction et transformation des CSV

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
Extrapolation sur la nuit complète
```bash
Les données couvrent 1h de CSV et 2h d’événements, la nuit dure 7h.
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

# Traitement et alimentation de la bdd

Dans la bdd (avec MySQL Worbench), il faudra remplir la table resultat_nuit avec les informations présente d'une part dans la bdd et d'autre part avec les données des csv. Pour se faire on va :

Création d'une procedure dans SQL pour alimenter la table résultat nuit de la bdd
```bash
Création de la procédure 'insert_data_resultat'
```
Dans un second temps il faudra appeler cette procedure dans python pour pouvoir y intégrer les données récupérées en CSV.
```bash
Utilisation de MySQL connector et appel de la procedure et des données CSV à y intégrer.
Pour permettre une meilleure sécurisation des mots de passes. Nous avons créer des variables génériques et nos mots de passes individuel dans des fichiers non suivit par Git.
```
Les fichiers crées pour réaliser ces étapes sont :
```bash
- procedure_insertion.py
- ugrade_bdd.txt (Où se trouve la procédure à intégerer à la bdd vu que celle-ci n'est pas suivit par Git)
```
# Générer un rapport pour le médecin

L'objectif est ici que le médecin puisse consulter tous les résultats de la nuit d'étude du patient traités et non pas brut. Afin de pouvoir prescrirpar la suite un traitement adapté au patient.

# Création d'un datalake pour entrainer une IA

Pour créer le datalake :
Création du fichier database.py


# Création d'une route API pour permettre des connexions sécuriser avec des accés spécifique à la Bdd.


