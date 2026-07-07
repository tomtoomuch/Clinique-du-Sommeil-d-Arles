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

```

Afin de mener à bien les objectifs fixés, nous avons, suite à une lecture attentive du brief et à la suite d'une séance de brainstorming, identifié les différentes taches, sous-taches et compétences requises et avons mis en place un tableau Trello en fonction des souhaits, des compétences et des aspirations de chacun. (https://trello.com/b/Vuckm2dk).

```
![Vue Trello du groupe](./img/Trello.png "Vue Trello de la répartition des taches")

```

Nous avons également utilisé Git et Github afin de sauvegarder nos codes, de conserver un historique des modifications, en respectant les règles de contributions mises en place :

```

![Vue Contributing](./img/contributiong.png "Vue Contributing")




C17. **Développer les composants techniques et les interfaces d'une application** en utilisant les outils et langages de programmation adaptés et en respectant les spécifications fonctionnelles et techniques, les standards et normes d'accessibilité, de sécurité et de gestion des données en vigeur dans le but de répondre aux besoins fonctionnels identifiés.

```

Pour mener à bien ces taches, nous avons utilisé :

 - Des dépots Github permettant un versionnement des sources (Pour le frontEnd : https://github.com/arcar/CliniquePlus---Prototype-d-interface-utilisateur.git, pour le Back-End : https://github.com/tomtoomuch/Clinique-du-Sommeil-d-Arles.git)

 - Pour la partie Front-End : 
    ANGULAR composée d'une page d'accueil, d'une page de connexion qui permet l'authentification des utilisateurs et de les répartir en 3 catégories ( Infirmiers, Médecins, RH). 
    En fonction de la catégorie authentifiée, le composant header affiche des éléments différents qui sont:

    - pour les médecins : un lien "dashboard" qui permet d'ouvrir un onglet affichant les rendus générés  via streamlit par le fichier dashboard_cpap.py, un lien "rapport nuit" qui permet d'ouvrir un onglet affichant les rendus générés via streamlit par le fichier app_resultats_nuit_avec_ia.py

    - pour les rh : un lien qui permet d'ouvrir un nouveau composant rendant possible la sélection d'un employé afin d'en afficher le profil et d'en modifier les éléments (nom, prenom, email, telephone, actif)

    - pour les infirmiers : un lien "analyse nuit" qui ouvre un composant permettant de choisir la nuit à analyser, de choisir le médecin validateur, de rentrer un commentaire médical et de valider, lançant ainsi l'ETL1 avec ces 3 composants obligatoires; un lien "suivi cpap jour" qui ouvre un composant permettant de choisir le patient qui aura ses relevés cpap jour analysés et de valider en lançant l'ETL2.
```
![Angular](./img/angular.png "Vue Angular CliniquePlus")

```

Pour le composant permettant la selection d'une nuit, d'un médecin validateur et l'ajout d'un commentaire médical et le lancement de l'ETL, voici la méthode :

```
```ts

// Déclarations des interfaces qui servent à décrire la forme que doivent avoir les différents objets

interface Nuit {
  id_nuit: number;
}

interface ApiResponse {
  success: boolean;
  message: string;
  nuitsTrouvees: Nuit[];
}

interface Medecin {
  id_personnel: number;
  nom: string;
  prenom: string;
  specialite: string;
  numero_rpps: string;
  date_embauche: string;
  telephone: string;
  email: string;
  actif: number;
  password: string;
}


```
```ts
export class AnalyseNuit implements OnInit {

  commentForm: FormGroup;  // Déclaration du formulaire

  nuits: Nuit[] = [];       //déclaration d'une variable nuits qui est un tableau nommé Nuit vide au démarrage du composant
  docs: Medecin[] = [];

  loadingNuits = false;
  loadingMedecins = false;
```
```ts
  this.commentForm = this.fb.group({        //Création de la structure du formulaire
      selectedNuit: [null, Validators.required],          //Attend qu'une nuit soit selectionnée pour que le champ du formulaire soit validé
      selectedMedecin: [null, Validators.required],     //Attend qu'un médecin soit selectionné pour que le champ du formulaire soit validé
      comment: ['', [Validators.required, Validators.minLength(3)]]     //Attend qu'un commentaire de plus de 3 lettres soit rentré pour que le champ soit validé
    });

```
```ts
ngOnInit(): void {          //Fonctions qui seront exécutées dès le chargement du composant pour récupérer la liste des nuits et des medecins disponibles
    console.log('INIT AnalyseNuit');
    this.loadNuits();
    this.loadMedecins();
  }
```
```ts
 loadMedecins() {       //Fonction qui charge la liste des médecins depuis l'API
    this.loadingMedecins = true;    // Pour affichage HTML de l'état du chargement

    this.routes.listeMedecins().subscribe({    // Appel de l'API via le service "routes" et subscribe permet de récuperer la réponse quand elle arrive
      next: (response: any) => {  // réponse quand l'API répond correctement

        this.docs = response.medecin ?? []; // stockage de la réponse dans le tableau "docs" et si pas de valeur, tableau vide (??[])

        this.loadingMedecins = false;

        this.cdr.detectChanges(); //detecte les changements pour mettre a jour le HTML

        console.log('loaded medecins:', this.docs);
      },
      error: (err) => {     //En cas d'erreur
        console.error(err);
        this.loadingMedecins = false;
      }
    });
  }
```
```ts
 submit() {

    if (this.commentForm.invalid) return;  //ici on verifie si le formulaire est valide et si non, on arrête

    const { selectedNuit, selectedMedecin, comment } = this.commentForm.value;  //On récupère les valeurs du formulaire

    if (!selectedNuit || !selectedMedecin) { //On verifie à nouveau que les champs ne sont pas vides sinon on arrête
      alert("Sélection manquante.");
      return;
    }

    this.routes.lancerETL1(     // Appel de l'API via le service "routes" avec les 3 parametres et subscribe permet de récuperer la réponse quand elle arrive
      selectedNuit.id_nuit,
      selectedMedecin.id_personnel,
      comment
    ).subscribe({
      next: (res) => {  // si API répond correctement
        console.log("ETL lancé :", res);
          
        // reset après réussite
        this.commentForm.reset();
      },
      error: (err) => {     // si erreur
        console.error("Erreur ETL :", err);
        console.log(err.error);
      }
    });
  }
```

```
- Pour la partie Back-End : 

    - Python pour le nettoyage des données, le calcul des indicateurs, la création du rapport médical, la génération des courbes, l'enregistrement des données dans un datalake, l'alimentation d'une base sqlite analytique

    - JavaScript avec Express et NodeJs pour la création de l'API permettant l'utilisation de routes et requètes nécessaires à la communication entre le front et le back

    - Streamlit pour les résultats des nuits avec prédiction de comorbidités

```


## Ainsi que C8, C9 et C10 **si traité**

C8. **Paramètre un service d'intelligence articielle** en suivant sa documentation technique et en respectant les spécifications du projet, afin de permettre l'intégration des connecteurs du service das le système d'information.

C9. **Développer une API exposant un modèle d'intelligence artificielle** en utilisant l'architecture REST pour mettre l'interaction entre le modèle et les autres composants.

C10. **Intégrer l'API d'un modèle ou d'un service d'intelligence artificielle** dans une application, en respectant les spécifications du projet et les normes d'accessibilité en vigeur, à l'aide de la documentation technique de l'API, afin de créer les fonctionnalités d'intelligence artificielle de l'application.


