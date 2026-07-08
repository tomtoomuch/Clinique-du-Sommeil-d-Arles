# RAPPORT DE REALISATION D'ETLs MULTIPLES SUR UN WORKFLOW D'ETUDE HOSPITALIERE

Ce projet d'ETL en 3 phases à destination des 

## C1, C2 : extraction et requêtes SQL (rappel ETL1, ETL3, mini ETL CPAP)
C1 . **Automatiser l'extraction de données** depuis un service web, une page web (scraping*), un fichier de données, une base de données et un système big data* en programmant le script* adapté afin de pérenniser la collecte des données nécessaires au projet. 
 
### Lola
**C2.Développer les requêtes de type SQL d'extraction des données** depuis un système de gestion de base de données et un système big data en appliquant le langage de requête propre au système afin de préparer la collecte des données nécessaires au projet.


**Alimentation_base_analytique**
Ce fichier est un ETL(3) qui a pour object d'alimenter la base_analytique.db avec les données de la base de donnée relationnelle de la Clinique du Sommeil d'Arles (cliniquenuitscompletes.sql).

  - Connexion du fichier à MySQL : 
*Nous avons choisi pour cette connexion de la sécuriser en mettant les données en dure (mot de passe, port et non de la base) dans un fichier non suivi par Git.* 

```bash
import mysql.connector
from mysql.connector import Error as MySQLError
from mdp import motdepasse, bdd, port

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": motdepasse,
    "database": bdd,
    "port": port,
    "use_pure": True
}
   - Connexion du fichier à Sqlite : 
```bash
import sqlite3

connexion = sqlite3.connect(chemin_db)
connexion.commit()
curseur.close()
```
   - Requête d'alimentation dim_temps : Afin d'alimenter la table dim_temps nous faisons cette requête directement stocké dans l'ETL car aucune donnée ne vient ici de MySQL. 
```bash
def charger_dim_temps (conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()

    # Dates de début et de fin
    date_debut = datetime(2020, 1, 1)
    date_fin = datetime(2027, 12, 31)

    # Initialisation
    date_courante = date_debut

    # Jours de la semaine
    jours = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche"
    ]

    while date_courante <= date_fin:

        id_temps = int(date_courante.strftime("%Y%m%d"))
        date_complete = date_courante.strftime("%Y-%m-%d")
        annee = date_courante.year
        mois = date_courante.month
        jour = date_courante.day
        trimestre = (mois - 1) // 3 + 1
        jour_semaine = jours[date_courante.weekday()]
        est_weekend = 1 if date_courante.weekday() >= 5 else 0

        cursor_sqlite.execute(
            "SELECT 1 FROM dim_temps WHERE id_temps = ?",
            (id_temps,)
        )

        if cursor_sqlite.fetchone() is None:
            cursor_sqlite.execute("""
                INSERT INTO dim_temps (
                    id_temps,
                    date_complete,
                    annee,
                    mois,
                    jour,
                    trimestre,
                    jour_semaine,
                    est_weekend
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_temps,
                date_complete,
                annee,
                mois,
                jour,
                trimestre,
                jour_semaine,
                est_weekend
            ))

        date_courante += timedelta(days=1)

        conn_sqlite.commit()

```

   - Requête récupération des données MySQL pour alimenter la table dim_patient :

```bash
def charger_dim_patient(id_patient, conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()
   
    conexion_mysql = None
    conexion_sqlite = None

# Récupération des données de la table patient dans MySQL
    try:
        conexion_mysql = get_mysql_connection()
        cursor_mysql = conexion_mysql.cursor(dictionary=True)

        conexion_sqlite = sqlite3.connect("base_analytique.db")
        cursor_sqlite = conexion_sqlite.cursor()

        query = """
            SELECT
                id_patient, nom, prenom, date_naissance, sexe,
                imc_initial, fumeur AS fumeur_initial,
                pa_tabac AS pa_tabac_initial, profession,
                niveau_activite, CURDATE() AS date_maj
            FROM patient
            WHERE id_patient = %s
        """

        cursor_mysql.execute(query, (id_patient,))
        fila = cursor_mysql.fetchone()

        if fila is None:
            print(f"Patient {id_patient} introuvable")
            return

# Intégration des données récupérées dans sqlite 
        cursor_sqlite.execute(
            """INSERT OR IGNORE INTO dim_patient
               (id_patient, nom, prenom, date_naissance, sexe, imc_initial,
                fumeur_initial, pa_tabac_initial, profession, niveau_activite, date_maj)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                int(fila["id_patient"]),
                str(fila["nom"]),
                str(fila["prenom"]),
                str(fila["date_naissance"]),
                str(fila["sexe"]),
                float(fila["imc_initial"]),
                str(fila["fumeur_initial"]),
                float(fila["pa_tabac_initial"]),
                str(fila["profession"]),
                str(fila["niveau_activite"]),
                str(fila["date_maj"]),
            )
        )

        conexion_sqlite.commit()
        print(f"Patient {id_patient} traité")

    finally:
        if conexion_mysql is not None and conexion_mysql.is_connected():
            conexion_mysql.close()

        if conexion_sqlite is not None:
            conexion_sqlite.close()

    conn_sqlite.commit()
```
   - Création de la procédure dans MySQL **recuperation_donnees_pour_faits_nuits_base_**  
```bash
CREATE DEFINER=`root`@`localhost` PROCEDURE `recuperation_donnees_pour_faits_nuit_base_analytique`(
IN p_id_patient INT
)
BEGIN 
  SELECT
        r.id_nuit,
        CAST(DATE_FORMAT(n.date_nuit, '%Y%m%d') AS UNSIGNED) AS id_temps,
		n.id_patient,
        r.iah,
        r.severite_iah,
        r.spo2_min,
        r.spo2_moy,
        r.spo2_mediane,
        r.nb_apnees,
        r.nb_hypopnees,
        r.nb_rera,
        r.nb_microeveils,
        r.duree_sommeil_min,
        r.duree_hypoxie_min,
        r.position_dominante,
        r.decibels_max,
        r.decibels_moy,
        r.nb_ronflements_forts,

        (
            SELECT MAX(s.id_suivi)
            FROM suivi_patient s
            WHERE s.id_patient = n.id_patient
        ) AS id_suivi_le_plus_proche,

        CASE
            WHEN r.nb_apnees = 0 THEN 0
            ELSE (
                SELECT COUNT(*)
                FROM evenement_respiratoire e
                WHERE e.id_nuit = r.id_nuit
                  AND e.type_evenement = 'apnée centrale'
            ) * 100.0 / r.nb_apnees
        END AS pct_apnees_centrales

    FROM resultat_nuit r
    JOIN nuit_etude n ON r.id_nuit = n.id_nuit
    WHERE n.id_patient = p_id_patient;
END
```
   
   - Appel de la procédure stocké "recuperation_donnees_pour_faits_nuit_base_analytique" dans MySQL pour alimenter la table fait_nuit :
```bash
def charger_fait_nuit(id_patient, conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()

    print([id_patient])
    conexion_mysql = get_mysql_connection()

#Récupération des données via la procédure
    df = pd.read_sql(
    "call cliniquesommeil2.recuperation_donnees_pour_faits_nuit_base_analytique(%s)",
    conexion_mysql,
    params=[id_patient]
)

    if df.empty:
        print(f"Patient {id_patient} introuvable")
    
    else:

        fila1= df.iloc[0]

#Insertion des données dans la base sqlite
        cursor_sqlite.execute (
        """INSERT OR IGNORE INTO faits_nuits
            (id_nuit,id_patient,id_temps,iah, severite_iah, spo2_min, spo2_moy, spo2_mediane, nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,duree_sommeil_min,
            duree_hypoxie_min, position_dominante, decibels_max, decibels_moy, nb_ronflements_forts, id_suivi_le_plus_proche, pct_apnees_centrales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            int (fila1["id_nuit"]),
            int (fila1["id_patient"]),
            int (fila1["id_temps"]),
            float(fila1["iah"]),
            str(fila1["severite_iah"]),
            float(fila1["spo2_min"]),
            float(fila1["spo2_moy"]),
            float(fila1["spo2_mediane"]),
            int(fila1["nb_apnees"]),
            int(fila1["nb_hypopnees"]),
            int(fila1["nb_rera"]),
            int(fila1["nb_microeveils"]),
            int(fila1["duree_sommeil_min"]),
            float(fila1["duree_hypoxie_min"]),
            str(fila1["position_dominante"]),
            float(fila1["decibels_max"]),
            float(fila1["decibels_moy"]),
            int(fila1["nb_ronflements_forts"]),
            int(fila1["id_suivi_le_plus_proche"]),
            float(fila1["pct_apnees_centrales"]),
        )
        )

    conn_sqlite.commit()
    conexion_mysql.close()
```



## C4 : modélisation des données (schéma Galaxy + dimsuivipatient)

**Créer une base de données** dans le respect du RGPD en élaborant les modèles conceptuels et physiques des données à partir des données préparées et en programmant leur import afin de stocker le jeu de données du projet.
- Non réaliser pour le moment


## C5 : API/accès aux données (procédures stockées utilisées)
**Développer une API mettant à disposition le jeu de données** en utilisant l'architecture REST afin de permettre l'exploitation du jeu de données par les autres composants du projet.
- ?


## C14,C15 : analyse du besoin et conception technique (vos choix d'architexture pour les 2 applications)
C14. **Analyser le besoin d'application d'un commanditaire intégrant un service d'intelligence artificielle**, en rédigeant les spécifications fonctionneles et en le modélisant, dans le respect des standards d'utilisabilité et d'accessibilité, afin d'établir avec précision les objectifs de développement correspondant au besin et à la faisabilité technique.
- ETL 1: est une interface qui répond aux besoins du médecin validateur d'avoir toutes les informations nécéssaires pour poser une diagnostique sur le patient et de pouvoir poser son diagnostic et de valider sur le même interface.
- ETL 3: permet en lien avec l'ETL1 d'automatiser l'alimentation de la base de données analytique pour l'entrainement de l'IA. Car plus celle-ci sera alimenter par les données de la clinique plus son taux de fiabilité pour les diagnostics (Obésité etc.), sera fiable.


### Lola
C15. **Concevoir le cadre technique d'une application integrant un service d'intelligence artificielle**, à partir de l'analyse du besoin, en spécifiant l'architecture technique et applicative et en préconisant les outils et méthodes de développement, pour permettre le développement du projet.

1. Identifier les besoins :
Cette interface s'adresse au médecin validateur désigné par l'oppérateur, pour lui permettre de visualiser toutes les informations de la nuit d'étude (rapport résultats de la nuit d'étude, la courbe spO2, la courbe du débit nasal et la courbe des ronflements). Mais aussi d'avoir une aide au diagnostic avec l'interprétation de l'IA basée sur les commorbidité du patient. Enfin toujours sur cette interface le médecin validateur pourra poser un diagnostic (via un commentaire médical de validation) et valider le rapport final. Rapport final qui sera par la suite enregistré dans le dossier du patient et téléchargé par le médecin.

2. Choisir la technologie
   - Pour l'application du médecin validateur on a choisit d'utiliser Streamlit, qui permet d'avoir rapidement une interface. 

   - Il faut également choisir l'IA qui est la plus adapré aux besoins identifiés précédemment. Ici nous utilisons l'IA de Random Forest, pour une application médicale. Random Forest (RF) est l'un des algorithmes les plus utilisés en IA médicale grâce à sa robustesse et son interprétabilité. On l'a choisi également car elle a un taux de réussite de 85% à 93% sur les prédictions des apnées du sommeil.

3. Architecture technique 
   - Création d'une application pour consulter les résultats et des nuits d'étude
   - Création d'un ETL (alimentation_base_analytique) afin de continuer à l'alimenter le modèle pour augmenter sa fiabilité.

4. Préconisation : 
   - Concernant l'interface elle est actuellement lente, si on souhaite partir sur une interface plus performante il faudra partir sur le même modèle que l'application Opérateur et utiliser de l'Angular.
   - Concernant l'utilisation de l'IA, continuer à l'alimenter avec les données récoltées. Impliquer les médecins dans l'entrainement de l'IA notamment pour l'interprétation des résultats de l'IA (prendre en concidération les dernières recherches).
    

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

### Lola
C21. **Résoudre les incidents techniques** en apportant les modifications nécessaires au code de l’application et en documentant les solutions pour en garantir le fonctionnement opérationnel.

Problème rencontré dans l'exécussion de l'ETL (alimentation_base_analytique) lors de son déclenchement par app_resultat_avec_ia.
```bash
sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 21152 and this is thread id 17492.
```
Le problème que nous avons rencontré ici est un conflit entre notre application Streamlit et Sqlite. Sqlite bloque, car Streamlit utilise un autre thread que la connexion sqlite. 
Pour remédier à ce problème nous avons consulter tchatGPT qui nous a conseillé de changer notre connexion Sqlite dans notre ETL, passer d'un niveau global au niveau des fonctions.
Nous avons donc supprimé la connexion global et nous avons intégré à chaque fonction lancé par l'ETL :
```bash
def charger_fait_nuit(id_patient, conn_sqlite):
    cursor_sqlite = conn_sqlite.cursor()
 conn_sqlite.commit()
```
