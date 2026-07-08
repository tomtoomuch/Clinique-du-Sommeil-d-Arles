# Registre des traitements de données à caractère personnel

## Centre de diagnostic et de traitement des troubles respiratoires du sommeil

**Version :** 2.0

**Cadre réglementaire**

* Règlement (UE) 2016/679 (RGPD)
* Code de la santé publique
* Référentiel HDS (Hébergeur de Données de Santé)
* Doctrine de la CNIL relative aux données de santé

---

# Cartographie des acteurs

## Responsable du traitement

La Clinique du Sommeil est responsable des traitements réalisés dans le cadre :

* de la consultation médicale ;
* du diagnostic ;
* de la prescription ;
* du suivi clinique ;
* de la coordination des soins.

## Responsables de traitement distincts

Les organismes suivants agissent généralement comme responsables de traitement pour leurs propres finalités :

* Prestataire de Santé à Domicile (PSAD)
* Fabricant du dispositif médical connecté (selon les traitements réalisés)
* Assurance Maladie
* Organisme complémentaire

Des conventions de partage de données ou des contrats de sous-traitance doivent préciser les responsabilités respectives conformément à l'article 26 (responsables conjoints) ou à l'article 28 (sous-traitance) du RGPD, selon les situations.

---

# Registre des traitements

## Traitement 1 – Gestion administrative des patients

**Finalité**

Gestion des admissions, rendez-vous, création du dossier patient, facturation.

**Données**

* identité : nom, prénom, date de naissance, sexe
* coordonnées : adresse, téléphone, email
* sécurité sociale : NIR


**Destinataires**

* secrétariat
* médecins
* comptabilité

---

## Traitement 2 – Dossier médical

**Finalité**

Suivi médical.

**Données**

* fumeur
* conso alcool
* examens
* comptes rendus
* comorbidités
* paramètres cliniques

---

## Traitement 3 – Examens du sommeil

**Données**

* polygraphie
* polysomnographie
* oxymétrie
* tension systolique et diastolique
* évènements respiratoires
* mouvements thoraciques

---

## Traitement 4 – Prescription d'un traitement PPC

**Finalité**

Prescription du dispositif médical.

**Données transmises au PSAD**

* identité
* coordonnées
* prescription
* diagnostic
* paramètres de pression
* compte rendu médical ??
* niveau de sévérité de l'apnée
* informations administratives nécessaires à la prise en charge

**Destinataires**

* prestataire de santé à domicile
* médecin prescripteur

---

# Traitement 5 – Installation du dispositif PPC (Prestataire)

Ce traitement est généralement réalisé sous la responsabilité propre du prestataire de santé à domicile. Ces données sont transmises depuis les relevés de la machine du prestataire à la Clinique du Sommeil.

## Données traitées

* coordonnées
* adresse d'installation
* numéro de série de l'appareil
* masque utilisé

## Finalités

* installation
* maintenance
* livraison
* renouvellement
* assistance technique

---

# Traitement 6 – Télésuivi des appareils PPC

Le dispositif peut transmettre automatiquement :

* heures d'utilisation
* observance
* IAH résiduel
* pression délivrée
* fuites
* évènements respiratoires
* type de masque
* alertes techniques
* données de fonctionnement

## Destinataires

### Centre du sommeil

Suivi thérapeutique.

### Prestataire

Maintenance. Observance.

### Fabricant (selon le modèle)

Maintenance des plateformes connectées.

---

# Traitement 7 – Suivi de l'observance

Objectifs :

* vérifier l'efficacité
* adapter le traitement
* répondre aux exigences de remboursement lorsque la réglementation le prévoit

Données :

* durée moyenne d'utilisation
* utilisation quotidienne
* interruptions
* indice d'apnées résiduelles

Les échanges entre le centre et le PSAD sont limités aux données strictement nécessaires.

---

# Traitement 9 – Gestion des alertes

Alertes possibles :

* arrêt du traitement
* mauvaise observance
* fuite importante
* panne
* pression anormale
* masque défectueux

Actions :

* appel du patient
* consultation
* intervention technique
* renouvellement du matériel

---

# Traitement 10 – Facturation

Flux :

Centre → Assurance Maladie

Prestataire → Assurance Maladie

Prestataire → Complémentaire santé

---

# Traitement 11 – Coordination des soins

Échanges avec :

* médecin traitant
* pneumologue
* ORL
* cardiologue
* neurologue
* diabétologue

Documents :

* comptes rendus
* prescriptions
* évolution thérapeutique

---

# Flux de données

## Centre → Prestataire PPC

Transmission :

* ordonnance
* identité
* coordonnées
* diagnostic
* paramètres PPC
* urgence éventuelle

## Prestataire → Centre

Transmission :

* installation réalisée
* incidents
* observance
* difficultés du patient
* remplacement du matériel
* alertes

## Appareil → Plateforme HDS

Transmission automatique :

* télémétrie
* données d'observance
* paramètres techniques

## Plateforme HDS → Centre

Accès sécurisé des professionnels habilités.

## Plateforme HDS → Prestataire

Accès limité aux données nécessaires à la maintenance et au suivi logistique.

---

# Base juridique

## Centre du sommeil

* exécution de la mission de soins ;
* obligations légales ;
* prise en charge médicale.

## Prestataire de santé à domicile

* exécution du contrat de fourniture et de maintenance du dispositif médical ;
* obligations réglementaires ;
* continuité des soins.

---

# Mesures de sécurité

## Organisationnelles

* gestion des habilitations
* politique de mots de passe
* confidentialité contractuelle
* formation RGPD
* revue annuelle des accès

## Techniques

* hébergement HDS
* authentification multifacteur
* chiffrement TLS
* journalisation
* sauvegardes
* supervision
* tests de restauration

---

# Analyse des risques

| Risque                                       | Gravité     | Mesures                                                |
| -------------------------------------------- | ----------- | ------------------------------------------------------ |
| Divulgation des données médicales            | Très élevée | Chiffrement, contrôle des accès                        |
| Mauvais destinataire                         | Élevée      | Double contrôle des envois                             |
| Cyberattaque                                 | Très élevée | EDR, PRA, sauvegardes                                  |
| Vol d'identifiants                           | Élevée      | MFA                                                    |
| Perte d'un ordinateur portable               | Élevée      | Chiffrement du disque                                  |
| Mauvaise synchronisation des plateformes PPC | Moyenne     | Contrôles automatiques et audits                       |
| Accès excessif par un prestataire            | Élevée      | Principe du moindre privilège et revues d'habilitation |

---

# Sous-traitants et partenaires

Le registre doit préciser pour chacun :

* raison sociale ;
* rôle (responsable de traitement, responsable conjoint ou sous-traitant) ;
* catégories de données traitées ;
* localisation de l'hébergement ;
* certification HDS le cas échéant ;
* durée de conservation ;
* mesures de sécurité ;
* existence d'un contrat conforme à l'article 28 du RGPD lorsque le partenaire agit comme sous-traitant.

Une attention particulière doit être portée aux plateformes de télésuivi fournies par les fabricants de PPC : selon les modalités contractuelles et les finalités poursuivies (maintenance, amélioration des dispositifs, services numériques), ces acteurs peuvent intervenir comme sous-traitants ou comme responsables de traitement distincts. Cette qualification doit être analysée et formalisée.

---

# Recommandations complémentaires

Le Centre du Sommeil devrait disposer des documents suivants :

1. Registre des traitements (présent document).
2. Cartographie des flux de données.
3. Politique d'habilitation des utilisateurs.
4. Procédure de gestion des violations de données.
5. Procédure d'exercice des droits des patients.
6. Modèle de convention d'échange de données avec les PSAD.
7. Clauses de protection des données intégrées aux contrats avec les prestataires.
8. Analyse d'impact relative à la protection des données (AIPD) lorsque les traitements présentent un risque élevé, notamment en raison du volume de données de santé traitées et de la télésurveillance.
