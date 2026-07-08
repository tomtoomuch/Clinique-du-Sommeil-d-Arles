# RAPPORT DE REALISATION D'ETLs MULTIPLES SUR UN WORKFLOW D'ETUDE HOSPITALIERE

Ce projet d'ETL en 3 phases à destination des 

## C1, C2 : extraction et requêtes SQL (rappel ETL1, ETL3, mini ETL CPAP)
C1 . **Automatiser l'extraction de données** depuis un service web, une page web (scraping*), un fichier de données, une base de données et un système big data* en programmant le script* adapté afin de pérenniser la collecte des données nécessaires au projet. 

# Présentation globale du projet

Le projet **Clinique du Sommeil d'Arles** a pour objectif d'automatiser le traitement des données des nuits d'étude afin d'aider les professionnels de santé dans le diagnostic, le suivi des patients et l'exploitation analytique des données.

Le système s'appuie sur trois applications métiers :

- **Application Opérateur** : permet à l'infirmier de sélectionner une nuit d'étude à traiter, choisir le médecin validateur, saisir un commentaire médical et lancer automatiquement l'ETL1.

- **Application Résultats Nuit avec IA** : permet de consulter les résultats de la nuit, visualiser les courbes et le rapport médical, afficher une prédiction de comorbidités grâce à un modèle Random Forest, ajouter le commentaire du médecin, valider le diagnostic, déclencher l’ETL3 et générer automatiquement le PDF du patient.

- **Dashboard CPAP** : permet de suivre quotidiennement les patients traités par CPAP, consulter les alertes, les indicateurs de suivi et les statistiques d'utilisation.

Pour alimenter ces applications, trois pipelines ETL ont été développés :

- **ETL1** traite une nuit d'étude complète à partir du fichier CSV des capteurs et des événements respiratoires stockés dans MySQL. Il calcule les indicateurs médicaux, alimente la base opérationnelle MySQL, génère le rapport médical et les courbes, puis alimente le datalake SQLite avec les données brutes et les données préparées.

- **ETL2** importe les données quotidiennes de suivi CPAP depuis un fichier CSV, calcule automatiquement les alertes métier (observance < 4 h et IAH résiduel > 5) et alimente la table faits_suivi_cpap_jour de la base analytique SQLite. Ces données sont ensuite exploitées par le Dashboard CPAP.

- **ETL3** extrait les données médicales validées de la base opérationnelle MySQL et alimente la base analytique SQLite (modèle galaxie). Cette base est utilisée par le Dashboard CPAP pour les analyses et par le module d'intelligence artificielle pour entraîner les modèles de prédiction des comorbidités.


## Focus sur l'ETL1

### Objectif

L'ETL1 automatise le traitement complet d'une nuit d'étude polysomnographique. Il est lancé depuis l'application Opérateur après que l'infirmier sélectionne une nuit, choisisse le médecin validateur et saisisse un commentaire médical.

---

## Technologies utilisées

- Python
- Pandas
- MySQL
- SQLite (Datalake)
- Matplotlib
- Streamlit (prototype) / Angular-Express (application)
- Git / GitHub

---

## Fonctionnement de l'ETL

### 1. Extraction

Le pipeline recherche automatiquement le fichier CSV correspondant à l'identifiant de la nuit, puis le charge avec Pandas.

```bash
chemin_csv, id_patient = trouver_csv_depuis_id_nuit(id_nuit)

df = lire_csv_capteur(chemin_csv)
```

Le script vérifie également que le fichier existe et que toutes les colonnes obligatoires sont présentes.

---

### 2. Transformation

Les indicateurs médicaux sont calculés automatiquement à partir du signal :

- SpO₂ minimale, moyenne et médiane
- durée d'hypoxie
- position dominante
- intensité des ronflements
- nombre de ronflements forts

```bash
def calculer_indicateurs_signal(df, duree_nuit_min):
```

Cette fonction transforme les données brutes du capteur en indicateurs médicaux (SpO₂, IAH, hypoxie, ronflements, position dominante…) qui seront enregistrés dans MySQL.
---

### 3. Chargement

Les indicateurs sont transmis à une procédure stockée MySQL afin de créer le résultat médical de la nuit.

```bash
curseur.callproc(
    "sp_creer_resultat_nuit",
    [...]
)
```

Le pipeline génère ensuite :

- le rapport médical (.txt),
- les courbes (PNG),
- l'alimentation du datalake SQLite (raw_capteur et curated_nuit).

```bash
generer_rapport_texte(resultat, dossier_sortie)

generer_courbes(df, id_nuit, dossier_sortie)

initialiser_datalake()

alimenter_raw_capteur(df, id_nuit)

alimenter_curated_nuit(id_nuit, resultat)

```

---

### 4. Gestion des erreurs

Le pipeline prévoit une gestion des erreurs afin d'assurer la fiabilité du traitement.

- fichier CSV introuvable ;
- erreur lors de l'exécution des opérations MySQL.

Exemples :

```bash
if not os.path.exists(chemin_fichier):
    raise FileNotFoundError(
        f"Le fichier {chemin_fichier} est introuvable."
    )


except MySQLError as erreur:
    raise RuntimeError(
        f"Erreur MySQL lors de l'appel à la procédure stockée : {erreur}"
    ) from erreur
```

---

## Résultat obtenu

À la fin de l'exécution :

- le résultat médical est enregistré dans **MySQL** ;
- le rapport et les courbes sont générés automatiquement ;
- le datalake SQLite est alimenté ;
- le fichier CSV est déplacé dans le dossier `raw/traite`.


## Conclusion

L’ETL1 répond à la compétence C1 car il automatise l’ensemble du processus d’extraction, de transformation et de chargement (ETL) des données. Il récupère automatiquement les données provenant du fichier CSV et de MySQL, calcule les indicateurs médicaux, génère les documents nécessaires et alimente les bases de données utilisées par les applications métiers.



C2. **Développer les requêtes de type SQL d'extraction des données** depuis un système de gestion de base de données et un système big data en appliquant le langage de requête propre au système afin de préparer la collecte des données nécessaires au projet.
- ETL 3: Est un pipeline qui permets d'alimenter la base de données relationnel et la base de données analytique.

## C4 : modélisationdes données (schéma Galaxy + dimsuivipatient)

**Créer une base de données** dans le respect du RGPD en élaborant les modèles conceptuels et physiques des données à partir des données préparées et en programmant leur import afin de stocker le jeu de données du projet.
- Non réaliser pour le moment

## C5 : API/accès aux données (procédures stockées utilisées)
**Développer une API mettant à disposition le jeu de données** en utilisant l'architecture REST afin de permettre l'exploitation du jeu de données par les autres composants du projet.
- ?

## C14,C15 : analyse du besoin et conception technique (vos choix d'architexture pour les 2 applications)
C14. **Analyser le besoin d'application d'un commanditaire intégrant un service d'intelligence artificielle**, en rédigeant les spécifications fonctionneles et en le modélisant, dans le respect des standards d'utilisabilité et d'accessibilité, afin d'établir avec précision les objectifs de développement correspondant au besin et à la faisabilité technique.

# C14 – Analyser le besoin et modéliser l'application

## Contexte

Avant de développer les applications, nous avons réalisé une analyse fonctionnelle afin d'identifier les besoins des utilisateurs, les différentes étapes du traitement et les interactions entre les applications, les pipelines ETL et les bases de données.

L'objectif est de garantir un parcours utilisateur cohérent avant le développement technique.

---

## Architecture fonctionnelle

La figure suivante présente l'architecture fonctionnelle du projet ainsi que le parcours utilisateur, les applications développées, les pipelines ETL et les interactions entre les différentes bases de données.

![Architecture fonctionnelle du projet](architecture_c14.png)

*Figure 1 – Architecture fonctionnelle du projet Clinique du Sommeil d'Arles.*

Cette modélisation permet de comprendre le fonctionnement global du système :

1. Le patient réalise une nuit d'étude.
2. Les événements respiratoires sont enregistrés dans MySQL et les données des capteurs sont récupérées depuis un fichier CSV.
3. L'opérateur sélectionne la nuit, choisit le médecin validateur et ajoute un commentaire infirmier.
4. L'application Opérateur déclenche automatiquement l'ETL1.
5. L'ETL1 traite les données, calcule les indicateurs médicaux, met à jour MySQL, génère le rapport médical, les courbes et alimente le datalake SQLite.
6. Le médecin consulte ensuite les résultats dans l'application Résultats avec IA, ajoute son commentaire et valide le diagnostic.
7. Cette validation déclenche automatiquement l'ETL3, qui alimente la base analytique (modèle galaxie).
8. La base analytique est ensuite utilisée par le Dashboard CPAP ainsi que par le module de prédiction des comorbidités basé sur un modèle Random Forest.

---

## User Stories

### User Story 1

**En tant qu'opérateur**, je souhaite sélectionner une nuit d'étude, choisir un médecin validateur et lancer automatiquement le traitement afin de générer le rapport médical.

### User Story 2

**En tant que médecin**, je souhaite consulter les résultats de la nuit, confirmer le diagnostic et générer le PDF du patient afin d'alimenter la base analytique utilisée par le service d'intelligence artificielle.

---

## Critères d'acceptation

Le scénario est considéré comme valide lorsque :

- le diagnostic est confirmé ;
- le PDF du patient est généré ;
- l'ETL3 est exécuté automatiquement ;
- la base analytique est correctement alimentée.

---

## Accessibilité

Les applications ont été conçues en respectant des principes simples d'utilisabilité :

- navigation intuitive ;
- boutons clairement identifiés ;
- vocabulaire compréhensible ;
- limitation du nombre d'étapes pour chaque utilisateur.

---

## Conclusion

Cette analyse fonctionnelle nous a permis de définir les besoins métier, de modéliser le parcours utilisateur et d'identifier précisément le rôle des applications, des pipelines ETL et des bases de données avant le développement du projet.



C15. **Concevoir le cadre technique d'une application integrant un service d'intelligence artificielle**, à partir de l'analyse du besoin, en spécifiant l'architecture technique et applicative et en préconisant les outils et méthodes de développement, pour permettre le développement du projet.

## C16,C17 : réalisation technique (composants développés)

C16. **Coordonner la réalisation technique d'une application d'intelligence artificielle** en s'intégrant dans une conduite agile du projet et en contexte MLOps et en facilitant les temps de collaboration dans le but d'atteindre les objectifs de production et de qualité.

Afin de mener à bien les objectifs fixés, nous avons, à la suite d'une séance de brainstorming, mis en place un tableau Trello et réparti les différentes tâches en fonction des souhaits, des compétences et des aspirations de chacun. (https://trello.com/b/Vuckm2dk).


C17. **Développer les composants techniques et les interfaces d'une application** en utilisant les outils et langages de programmation adaptés et en respectant les spécifications fonctionnelles et techniques, les standards et normes d'accessibilité, de sécurité et de gestion des données en vigeur dans le but de répondre aux besoins fonctionnels identifiés.


Pour mener à bien ces taches, nous avons utilisé :
 
 - Des dépots Github permettant un versionnement des sources (Pour le frontEnd : https://github.com/arcar/CliniquePlus---Prototype-d-interface-utilisateur.git, pour le Back-End : https://github.com/tomtoomuch/Clinique-du-Sommeil-d-Arles.git)

 - Pour la partie Front-End : 
    ANGULAR composée d'une page d'accueil, d'une page de connexion qui permet l'authentification des utilisateurs et de les répartir en 3 catégories ( Infirmiers, Médecins, RH). 
    En fonction de la catégorie authentifiée, le composant header affiche des éléments différents qui sont:

        - pour les médecins : un lien "dashboard" qui permet d'ouvrir un onglet affichant les rendus générés  via streamlit par le fichier dashboard_cpap.py, un lien "rapport nuit" qui permet d'ouvrir un onglet affichant les rendus générés via streamlit par le fichier app_resultats_nuit_avec_ia.py

        - pour les rh : un lien qui permet d'ouvrir un nouveau composant rendant possible la sélection d'un employé afin d'en afficher le profil et d'en modifier les éléments (nom, prenom, email, telephone, actif)
        
        - pour les infirmiers : un lien "analyse nuit" qui ouvre un composant permettant de choisir la nuit à analyser, de choisir le médecin validateur, de rentrer un commentaire médical et de valider, lançant ainsi l'ETL1 avec ces 3 composants obligatoires; un lien "suivi cpap jour" qui ouvre un composant permettant de choisir le patient qui aura ses relevés cpap jour analysés et de valider en lançant l'ETL2.

- Pour la partie Back-End : 

        - Python pour le nettoyage des données, le calcul des indicateurs, la création du rapport médical, la génération des courbes, l'enregistrement des données dans un datalake, l'alimentation d'une base sqlite analytique

        - JavaScript avec Express et NodeJs pour la création de l'API permettant l'utilisation de routes et requètes nécessaires à la communication entre le front et le back

        - Streamlit pour les résultats des nuits avec prédiction de comorbidités


## Ainsi que C8, C9 et C10 **si traité**

C8. **Paramètre un service d'intelligence articielle** en suivant sa documentation technique et en respectant les spécifications du projet, afin de permettre l'intégration des connecteurs du service das le système d'information.

C9. **Développer une API exposant un modèle d'intelligence artificielle** en utilisant l'architecture REST pour mettre l'interaction entre le modèle et les autres composants.

C10. **Intégrer l'API d'un modèle ou d'un service d'intelligence artificielle** dans une application, en respectant les spécifications du projet et les normes d'accessibilité en vigeur, à l'aide de la documentation technique de l'API, afin de créer les fonctionnalités d'intelligence artificielle de l'application.


