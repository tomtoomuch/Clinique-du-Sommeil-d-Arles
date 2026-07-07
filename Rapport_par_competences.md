# RAPPORT DE REALISATION D'ETLs MULTIPLES SUR UN WORKFLOW D'ETUDE HOSPITALIERE

Ce projet d'ETL en 3 phases à destination des 

## C1, C2 : extraction et requêtes SQL (rappel ETL1, mini ETL CPAP)

## C4 : modélisation des données (schéma Galaxy + dimsuivipatient)

## C5 : API/accès aux données (procédures stockées utilisées)

## C14,C15 : analyse du besoin et conception technique (vos choix d'architecture pour les 2 applications)

## C16,C17 : réalisation technique (composants développés)

Afin de mener à bien les objectifs fixés, nous avons, à la suite d'une séance de brainstorming, mis en place un tableau Trello et réparti les différentes tâches en fonction des souhaits, des compétences et des aspirations de chacun. (https://trello.com/b/Vuckm2dk).

Pour mener à bien ses taches, nous avons utilisé :
 
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





CT5, CT6 : partage de connaissances et présentation (synthèse claire des limites identifiées en partie 6, justification des choix)
Ainsi que C8, C9 et C10 si traité