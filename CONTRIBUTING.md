// CONTRIBUTING.md

# Règles de contribution du projet.

> Ce document établit les rêgles de contribution au projet de SI 'métiers' de la Clinique du Sommeil d'Arles.

Une branche ```dev``` reçoit les contributions au développement à valider. Soyons attentifs à fabriquer et maintenir un code propre et bien commenté afin de faciliter les apports de chacun à tout instant.


## Convention de nommages

### Les branches

Chaque utilisateur crée sa branche en utilisant son blaze ou son prénom. 
```
git branch tonprenomoupseudo
```

Afin d'obtenir plus de clarté dans l'arbre de commits et une meilleure compréhension des contributions, il est souhaitable de définir une branche par tâche. Ces branches peuvent être fusionnées directement avec la branche de développement ```dev``` avant d'être poussées.
```
feat/nom-de-la-fonctionnalite

fix/correction-apportee

doc/nom-de-la-doc

data/nom-de-la-tache

_py/nom-du-script_
```

### Les commits

Encore une fois, pour garantir clarté et compréhension des contributions. Nous veillerons à nommer nos commits selon 

```console
<feat> Ajout de la fonctionnaliité

<fix> Correction réalisée

<data> Correction, amélioration apportée

<docs> Mise à jour du README
```

## Règles obligatoires pour les pull requests:

• une branche par ticket

• une Pull Request par ticket

• pas de push direct sur main

• pas de push direct sur develop, sauf consigne explicite

• validation obligatoire par l'intégrateur avant fusion
