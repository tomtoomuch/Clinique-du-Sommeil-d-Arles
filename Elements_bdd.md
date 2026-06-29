# UTILISATEURS ET PERMISSIONS

1. admin_bdd 
   - tous droits ouverts sert pour les opérations de maintenance et de modofications lourdes de la BDD

2. infirmier(ière)
   - peut accéder à la table **suivi_patient** *(SELECT, CREATE)*, avec un trigger pour bloquer l'accès au ID.
   - à la vue **nuit_disponible**

3. médecin
   - a le droit d'accéder à la table **patients** *(SELECT, UPDATE)*
   - à la table **suivi_patient** *(SELECT, UPDATE)*
   -  ainsi cas la vue **historique_patient**.

4. superviseur (infirmier(ère))
   - a le droit d'accéder à la vue **vue_infirmier_medecins_validateurs** 
   - et d'accéder à la table **résultats_nuit** *(SELECT, UPDATE)* -> saisir un  commentaire ainsi que le nom du médecin en service et validant les résultats.



# LES VUES

## Historique_patient
Cette vue a été crée pour permettre au **médecin** de voir rapidement le suivit qu'à eu le patient dans la clinique.

```bash
SELECT
    patient.nom,
    patient.prenom,
    consultation.date_consultation,
    prescription_nuit.id_prescription,
    nuit_etude.date_nuit,
    resultat_nuit.iah,
    suivi_patient.date_suivi,
    suivi_patient.statut_patient
FROM patient
LEFT JOIN consultation
    ON patient.id_patient = consultation.id_patient
LEFT JOIN prescription_nuit
    ON consultation.id_consultation = prescription_nuit.id_consultation
LEFT JOIN nuit_etude
    ON prescription_nuit.id_nuit = nuit_etude.id_nuit
LEFT JOIN resultat_nuit
    ON nuit_etude.id_nuit = resultat_nuit.id_nuit
LEFT JOIN suivi_patient
    ON patient.id_patient = suivi_patient.id_patient;
```

## Vue nuit_disponible
 On crée une vue pour **l'infirmier(ère)** puisse voir les nuits d'études qui ne sont pas rentrer dans résultats_nuit, pour pouvoir rentrer les résultats dans la table résultats_nuit par la suite.
```bash
  CREATE VIEW `nuit_disponible` AS
  SELECT nuit_etude.id_nuit
  FROM nuit_etude
  LEFT JOIN  resultat_nuit on nuit_etude.id_nuit = resultat_nuit.id_nuit
  WHERE resultat_nuit.id_resultat is null
```


## Vue vue_infirmier_medecins_validateurs
Cette vue a été crée pour que le **superviseur** puisse assigner un **médecin validateur**.
```bash
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `nuitsommeilfase2`.`vue_infirmier_medecins_validateurs` AS
    SELECT 
        `nuitsommeilfase2`.`medecin`.`id_personnel` AS `id_medecin`,
        `nuitsommeilfase2`.`personnel`.`nom` AS `nom`,
        `nuitsommeilfase2`.`personnel`.`prenom` AS `prenom`,
        `nuitsommeilfase2`.`medecin`.`numero_rpps` AS `numero_rpps`
    FROM
        (`nuitsommeilfase2`.`medecin`
        JOIN `nuitsommeilfase2`.`personnel` ON ((`nuitsommeilfase2`.`medecin`.`id_personnel` = `nuitsommeilfase2`.`personnel`.`id_personnel`)))
```

## Vue pour le medecin de prescription et consultation 
Cette vue permet au **médecin** d'avoir l'historique des consultations ainsi que les prescriptions, ce qui peut lui être utile pour le suivi du patient. 
```bash
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `nuitsommeilfase2`.`vue_medecin_consultation_prescription` AS
    SELECT 
        `nuitsommeilfase2`.`consultation`.`id_consultation` AS `id_consultation`,
        `nuitsommeilfase2`.`consultation`.`date_consultation` AS `date_consultation`,
        `nuitsommeilfase2`.`consultation`.`compte_rendu` AS `compte_rendu`,
        `nuitsommeilfase2`.`patient`.`nom` AS `nom_patient`,
        `nuitsommeilfase2`.`patient`.`prenom` AS `prenom_patient`,
        `nuitsommeilfase2`.`patient`.`numero_secu` AS `numero_secu_patient`,
        `nuitsommeilfase2`.`prescription_nuit`.`id_prescription` AS `id_prescription`,
        `nuitsommeilfase2`.`prescription_nuit`.`motif_prescription` AS `motif_prescription`,
        `nuitsommeilfase2`.`prescription_nuit`.`urgence` AS `urgence`
    FROM
        ((`nuitsommeilfase2`.`consultation`
        JOIN `nuitsommeilfase2`.`patient` ON ((`nuitsommeilfase2`.`consultation`.`id_patient` = `nuitsommeilfase2`.`patient`.`id_patient`)))
        LEFT JOIN `nuitsommeilfase2`.`prescription_nuit` ON ((`nuitsommeilfase2`.`consultation`.`id_consultation` = `nuitsommeilfase2`.`prescription_nuit`.`id_consultation`)))
```


# PROCEDURES
## Procedure pour inscrire les données dans la table résultat nuit.

Cette procédure a été modifié pour recevoir **l'ID du medecin validateur**.

```bash
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_creer_resultat_nuit`(
    IN p_id_nuit INT,
    IN p_id_medecin_validateur INT,
    IN p_spo2_min DECIMAL(5,2),
    IN p_spo2_moy DECIMAL(5,2),
    IN p_spo2_mediane DECIMAL(5,2),
    IN p_duree_hypoxie_min DECIMAL(6,2),
    IN p_position_dominante VARCHAR(20),
    IN p_decibels_max DECIMAL(5,2),
    IN p_decibels_moy DECIMAL(5,2),
    IN p_nb_ronflements_forts INT,
    IN p_duree_sommeil_min INT
)
BEGIN
    DECLARE v_nb_apnees INT DEFAULT 0;
    DECLARE v_nb_hypopnees INT DEFAULT 0;
    DECLARE v_nb_rera INT DEFAULT 0;
    DECLARE v_nb_microeveils INT DEFAULT 0;
    DECLARE v_duree_apnee_moy INT DEFAULT NULL;
    DECLARE v_duree_apnee_max INT DEFAULT NULL;
    DECLARE v_position VARCHAR(20);

    SET v_position = CASE
        WHEN LOWER(p_position_dominante) LIKE '%dors%' THEN 'dorsale'
        WHEN LOWER(p_position_dominante) LIKE '%lat%' THEN 'laterale'
        WHEN LOWER(p_position_dominante) LIKE '%vent%' THEN 'ventrale'
        ELSE 'mixte'
    END;

    -- Recupa©ration complaite depuis evenement_respiratoire
SELECT
    COUNT(CASE WHEN type_evenement LIKE '%apnee%' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'hypopnee' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'RERA' THEN 1 END),
    ROUND(AVG(duree_sec), 0),
    MAX(duree_sec)
INTO v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_duree_apnee_moy, v_duree_apnee_max
FROM evenement_respiratoire
WHERE id_nuit = p_id_nuit;

-- AJOUT NÃ‰CESSAIRE : extrapolation 2h a 7h (Ã—3.5)
-- SET v_nb_apnees    = ROUND(v_nb_apnees * 3.5);
-- SET v_nb_hypopnees = ROUND(v_nb_hypopnees * 3.5);
-- SET v_nb_rera        = ROUND(v_nb_rera * 3.5);

-- Micro-Ã©veils : maintenant calcule depuis les valeurs deja  extrapolees
SET v_nb_microeveils = v_nb_apnees + v_nb_hypopnees + v_nb_rera;
    -- Insertion avec extrapolation 2h â†’ 7h
    INSERT INTO resultat_nuit (
        id_nuit, id_medecin_validateur, date_validation,
        spo2_min, spo2_moy, spo2_mediane,
        duree_hypoxie_min, position_dominante,
        decibels_max, decibels_moy, nb_ronflements_forts,
        nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,
        duree_apnee_moy_sec, duree_apnee_max_sec,
        iah, duree_sommeil_min
    )
    VALUES (
        p_id_nuit,
        p_id_medecin_validateur,
        CURDATE(),
        p_spo2_min, p_spo2_moy, p_spo2_mediane,
        p_duree_hypoxie_min, v_position,
        p_decibels_max, p_decibels_moy, p_nb_ronflements_forts,
        v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_nb_microeveils,
        v_duree_apnee_moy, v_duree_apnee_max,
        ROUND((v_nb_apnees + v_nb_hypopnees)/(p_duree_sommeil_min/60), 2),   -- 
        p_duree_sommeil_min
    )
    ON DUPLICATE KEY UPDATE
        spo2_min = VALUES(spo2_min),
        spo2_moy = VALUES(spo2_moy),
        spo2_mediane = VALUES(spo2_mediane),
        duree_hypoxie_min = VALUES(duree_hypoxie_min),
        position_dominante = VALUES(position_dominante),
        decibels_max = VALUES(decibels_max),
        decibels_moy = VALUES(decibels_moy),
        nb_ronflements_forts = VALUES(nb_ronflements_forts),
        nb_apnees = VALUES(nb_apnees),
        nb_hypopnees = VALUES(nb_hypopnees),
        nb_rera = VALUES(nb_rera),
        nb_microeveils = VALUES(nb_microeveils),
        duree_apnee_moy_sec = VALUES(duree_apnee_moy_sec),
        duree_apnee_max_sec = VALUES(duree_apnee_max_sec),
        iah = VALUES(iah),
        duree_sommeil_min = VALUES(duree_sommeil_min),
        date_validation = CURDATE();

    SELECT 'OK' AS status,
           v_nb_apnees AS apnees,
           v_nb_hypopnees AS hypopnees,
           v_nb_microeveils AS microeveils,
           ROUND((v_nb_apnees + v_nb_hypopnees) /(p_duree_sommeil_min/60), 2) AS iah;
END
```
## Procedure pour le médecin ou infirmier(ère)

Cette procédure a été créée pour permettre par la recherche du suivi du patient par son du nom.

```bash
CREATE DEFINER=`root`@`localhost`
PROCEDURE `profil_patient`(
  IN p_nomPatient VARCHAR(30)
)
BEGIN
    SELECT *
    FROM patient
    LEFT JOIN suivi_patient
        ON patient.id_patient = suivi_patient.id_patient
    LEFT JOIN patient_comorbidite
        ON patient.id_patient = patient_comorbidite.id_patient
    LEFT JOIN comorbidite
        ON patient_comorbidite.id_comorbidite = comorbidite.id_comorbidite
    WHERE patient.nom = p_nomPatient;
END
```