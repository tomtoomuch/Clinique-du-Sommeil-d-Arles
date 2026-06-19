# Clinique-du-Sommeil-d-Arles-Pipeline-ETL-sur-nuit-d-tude
# Le projet
La Clinique du sommeil d'Arles, travail sur les maladies du sommeil.
Dans ce cadre ils vont passer par une étape de diagnostic du patient et dans un second temps le suivre pendant le traitement.
Lors de la nuit d'étude qui sert au diagnostic ils dispose de deux sources de données pour une nuit d’étude :

CSV capteur (signal brut sur 1h, 1 ligne / 10 secondes)
La table SQL evenement_respiratoire (événements respiratoires déjà détectés et validés sur 2h).

Ils ont besoins de regrouper les données pour pouvoir permettre au médecin d'avoir une vue d'ensemble pour faire le diagnostic.

# L'objectif
- Lire le CSV capteur
- Calculer les indicateurs cliniques
- Remplir la table resultatnuit avec les indicateurs cliniques du csv et de la table evenementrespiratoire
- Envoiyer le CSV dans le datalake pour usage futur (modèle en étoile faits_nuits)
- Produire un rapport médical avec diagnostic et courbes que le médecin pourra charger plus tard.

