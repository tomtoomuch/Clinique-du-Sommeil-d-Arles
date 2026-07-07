# RAPPORT DE REALISATION D'ETLs MULTIPLES SUR UN WORKFLOW D'ETUDE HOSPITALIERE

Ce projet d'ETL en 3 phases à destination des 

## C1, C2 : extraction et requêtes SQL (rappel ETL1, ETL3, mini ETL CPAP)
C1 . **Automatiser l'extraction de données** depuis un service web, une page web (scraping*), un fichier de données, une base de données et un système big data* en programmant le script* adapté afin de pérenniser la collecte des données nécessaires au projet. 
- ETL 1: C'est un front d'interface pour le médecin validateur (Streamlit) qui déclanche l'ETL3.  

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
- ETL 1: est une interface qui répond aux besoins du médecin validateur d'avoir toutes les informations nécéssaires pour poser une diagnostique sur le patient et de pouvoir poser son diagnostic et de valider sur le même interface.
- ETL 3: permet en lien avec l'ETL1 d'automatiser l'alimentation de la base de données analytique pour l'entrainement de l'IA. Car plus celle-ci sera alimenter par les données de la clinique plus son taux de fiabilité pour les diagnostics (Obésité etc.), sera fiable.

C15. **Concevoir le cadre technique d'une application integrant un service d'intelligence artificielle**, à partir de l'analyse du besoin, en spécifiant l'architecture technique et applicative et en préconisant les outils et méthodes de développement, pour permettre le développement du projet.

## C16,C17 : réalisation technique (composants développés)

C16. **Coordonner la réalisation technique d'une application d'intelligence artificielle** en s'intégrant dans une conduite agile du projet et en contexte MLOps et en facilitant les temps de collaboration dans le but d'atteindre les objectifs de production et de qualité.

C17. **Développer les composants techniques et les interfaces d'une application** en utilisant les outils et langages de programmation adaptés et en respectant les spécifications fonctionnelles et techniques, les standards et normes d'accessibilité, de sécurité et de gestion des données en vigeur dans le but de répondre aux besoins fonctionnels identifiés.


## Ainsi que C8, C9 et C10 **si traité**

C8. **Paramètre un service d'intelligence articielle** en suivant sa documentation technique et en respectant les spécifications du projet, afin de permettre l'intégration des connecteurs du service das le système d'information.

C9. **Développer une API exposant un modèle d'intelligence artificielle** en utilisant l'architecture REST pour mettre l'interaction entre le modèle et les autres composants.

C10. **Intégrer l'API d'un modèle ou d'un service d'intelligence artificielle** dans une application, en respectant les spécifications du projet et les normes d'accessibilité en vigeur, à l'aide de la documentation technique de l'API, afin de créer les fonctionnalités d'intelligence artificielle de l'application.


