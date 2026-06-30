-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: cliniquev3
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appareil`
--

DROP TABLE IF EXISTS `appareil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil` (
  `id_appareil` int NOT NULL AUTO_INCREMENT,
  `modele` varchar(100) NOT NULL,
  `numero_serie` varchar(100) DEFAULT NULL,
  `fabricant` varchar(100) DEFAULT NULL,
  `date_installation` date DEFAULT NULL,
  `statut` varchar(20) NOT NULL DEFAULT 'actif',
  `localisation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_appareil`),
  UNIQUE KEY `numero_serie` (`numero_serie`),
  CONSTRAINT `appareil_chk_1` CHECK ((`statut` in (_utf8mb4'actif',_utf8mb4'maintenance',_utf8mb4'hors service')))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil`
--

LOCK TABLES `appareil` WRITE;
/*!40000 ALTER TABLE `appareil` DISABLE KEYS */;
INSERT INTO `appareil` VALUES (1,'Natus Embla N7000','SN-PSG-001','Natus Medical','2018-03-01','actif','Salle PSG 1'),(2,'Natus Embla N7000','SN-PSG-002','Natus Medical','2018-03-01','actif','Salle PSG 2'),(3,'Natus Embla N7000','SN-PSG-003','Natus Medical','2019-06-15','actif','Salle PSG 3'),(4,'Somnoscreen Plus','SN-PSG-004','Somnomedics','2020-01-10','actif','Salle PSG 4'),(5,'Somnoscreen Plus','SN-PSG-005','Somnomedics','2020-01-10','maintenance','Salle PSG 5'),(6,'Natus Embla N7000','SN-PSG-006','Natus Medical','2021-04-01','actif','Réserve'),(7,'Alice 6 LDx','SN-PSG-007','Philips','2021-09-01','actif','Réserve'),(8,'Alice 6 LDx','SN-PSG-008','Philips','2022-02-01','actif','Réserve'),(9,'Somnoscreen Plus','SN-PSG-009','Somnomedics','2022-07-01','actif','Réserve'),(10,'Natus Embla N7000','SN-PSG-010','Natus Medical','2023-01-01','actif','Réserve'),(11,'AirSense 11','SN-CPAP-001','ResMed','2021-01-15','actif','Domicile patient'),(12,'AirSense 11','SN-CPAP-002','ResMed','2021-03-01','actif','Domicile patient'),(13,'AirSense 11','SN-CPAP-003','ResMed','2021-06-01','actif','Domicile patient'),(14,'DreamStation 2','SN-CPAP-004','Philips Respironics','2021-09-01','actif','Domicile patient'),(15,'DreamStation 2','SN-CPAP-005','Philips Respironics','2021-09-01','actif','Domicile patient'),(16,'AirSense 11','SN-CPAP-006','ResMed','2022-01-01','actif','Domicile patient'),(17,'AirSense 11','SN-CPAP-007','ResMed','2022-03-01','actif','Domicile patient'),(18,'DreamStation 2','SN-CPAP-008','Philips Respironics','2022-06-01','actif','Domicile patient'),(19,'AirSense 11','SN-CPAP-009','ResMed','2022-09-01','actif','Domicile patient'),(20,'AirSense 11','SN-CPAP-010','ResMed','2023-01-01','actif','Domicile patient'),(21,'DreamStation 2','SN-CPAP-011','Philips Respironics','2023-03-01','actif','Domicile patient'),(22,'AirSense 11','SN-CPAP-012','ResMed','2023-06-01','actif','Domicile patient'),(23,'AirSense 11','SN-CPAP-013','ResMed','2024-01-15','actif','Domicile patient'),(24,'AirSense 11','SN-CPAP-014','ResMed','2023-03-10','actif','Domicile patient'),(25,'DreamStation 2','SN-CPAP-015','Philips Respironics','2023-04-20','actif','Domicile patient'),(26,'AirSense 11','SN-CPAP-016','ResMed','2022-11-20','actif','Domicile patient'),(27,'AirSense 11','SN-CPAP-017','ResMed','2022-12-25','actif','Domicile patient'),(28,'DreamStation 2','SN-CPAP-018','Philips Respironics','2023-06-20','actif','Domicile patient'),(29,'AirSense 11','SN-CPAP-019','ResMed','2023-07-20','actif','Domicile patient'),(30,'AirSense 11','SN-CPAP-020','ResMed','2025-05-25','actif','Domicile patient');
/*!40000 ALTER TABLE `appareil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareil_cpap`
--

DROP TABLE IF EXISTS `appareil_cpap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil_cpap` (
  `id_appareil` int NOT NULL,
  `id_patient` int DEFAULT NULL COMMENT 'Patient auquel l appareil est attribué',
  `pression_initiale` decimal(4,1) DEFAULT NULL,
  `type_masque` varchar(50) DEFAULT NULL COMMENT 'nasal / facial / narinaire',
  `taille_masque` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_appareil`),
  KEY `fk_cpap_patient` (`id_patient`),
  CONSTRAINT `fk_appareil_cpap` FOREIGN KEY (`id_appareil`) REFERENCES `appareil` (`id_appareil`),
  CONSTRAINT `fk_cpap_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `appareil_cpap_chk_1` CHECK ((`pression_initiale` between 4 and 25))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil_cpap`
--

LOCK TABLES `appareil_cpap` WRITE;
/*!40000 ALTER TABLE `appareil_cpap` DISABLE KEYS */;
INSERT INTO `appareil_cpap` VALUES (11,NULL,8.0,'nasal','M'),(12,1,9.0,'facial','L'),(13,2,10.0,'nasal','M'),(14,NULL,10.0,'facial','M'),(15,NULL,8.5,'narinaire','M'),(16,NULL,9.5,'nasal','L'),(17,NULL,7.0,'facial','S'),(18,NULL,11.0,'nasal','M'),(19,NULL,8.0,'narinaire','S'),(20,NULL,9.0,'nasal','M'),(21,NULL,10.5,'facial','L'),(22,NULL,8.5,'nasal','M'),(23,NULL,8.0,'narinaire','S'),(24,NULL,9.0,'facial','L'),(25,NULL,10.0,'facial','M'),(26,NULL,10.0,'facial','XL'),(27,NULL,11.0,'facial','L'),(28,NULL,8.0,'nasal','M'),(29,NULL,9.0,'nasal','M'),(30,NULL,7.5,'narinaire','S');
/*!40000 ALTER TABLE `appareil_cpap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareil_psg`
--

DROP TABLE IF EXISTS `appareil_psg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil_psg` (
  `id_appareil` int NOT NULL,
  `version_firmware` varchar(50) DEFAULT NULL,
  `type_montage` varchar(50) DEFAULT NULL COMMENT 'complet / ambulatoire',
  PRIMARY KEY (`id_appareil`),
  CONSTRAINT `fk_appareil_psg` FOREIGN KEY (`id_appareil`) REFERENCES `appareil` (`id_appareil`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil_psg`
--

LOCK TABLES `appareil_psg` WRITE;
/*!40000 ALTER TABLE `appareil_psg` DISABLE KEYS */;
INSERT INTO `appareil_psg` VALUES (1,'4.2.1','complet'),(2,'4.2.1','complet'),(3,'4.2.3','complet'),(4,'3.1.0','ambulatoire'),(5,'3.1.0','ambulatoire'),(6,'4.3.0','complet'),(7,'2.5.1','complet'),(8,'2.5.1','complet'),(9,'3.2.0','ambulatoire'),(10,'4.3.1','complet');
/*!40000 ALTER TABLE `appareil_psg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bilan_mensuel_cpap`
--

DROP TABLE IF EXISTS `bilan_mensuel_cpap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bilan_mensuel_cpap` (
  `id_bilan` int NOT NULL AUTO_INCREMENT,
  `id_appareil` int NOT NULL,
  `annee` int NOT NULL,
  `mois` int NOT NULL,
  `duree_moy_h` decimal(4,2) DEFAULT NULL,
  `compliance_pct` decimal(5,2) DEFAULT NULL,
  `iah_residuel_moy` decimal(5,2) DEFAULT NULL,
  `fuites_moy` decimal(6,2) DEFAULT NULL,
  `nb_jours_utilises` int DEFAULT NULL,
  `nb_jours_non_utilises` int DEFAULT NULL,
  PRIMARY KEY (`id_bilan`),
  UNIQUE KEY `id_appareil` (`id_appareil`,`annee`,`mois`),
  KEY `idx_bilan_appareil_date` (`id_appareil`,`annee`,`mois`),
  CONSTRAINT `fk_bilan_appareil` FOREIGN KEY (`id_appareil`) REFERENCES `appareil_cpap` (`id_appareil`),
  CONSTRAINT `bilan_mensuel_cpap_chk_1` CHECK ((`annee` >= 2000)),
  CONSTRAINT `bilan_mensuel_cpap_chk_2` CHECK ((`mois` between 1 and 12)),
  CONSTRAINT `bilan_mensuel_cpap_chk_3` CHECK ((`compliance_pct` between 0 and 100)),
  CONSTRAINT `bilan_mensuel_cpap_chk_4` CHECK ((`nb_jours_utilises` >= 0)),
  CONSTRAINT `bilan_mensuel_cpap_chk_5` CHECK ((`nb_jours_non_utilises` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilan_mensuel_cpap`
--

LOCK TABLES `bilan_mensuel_cpap` WRITE;
/*!40000 ALTER TABLE `bilan_mensuel_cpap` DISABLE KEYS */;
/*!40000 ALTER TABLE `bilan_mensuel_cpap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comorbidite`
--

DROP TABLE IF EXISTS `comorbidite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comorbidite` (
  `id_comorbidite` int NOT NULL AUTO_INCREMENT,
  `libelle` varchar(100) NOT NULL,
  `categorie` varchar(50) DEFAULT NULL COMMENT 'cardiovasculaire / métabolique / respiratoire / psychiatrique / autre',
  PRIMARY KEY (`id_comorbidite`),
  UNIQUE KEY `libelle` (`libelle`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comorbidite`
--

LOCK TABLES `comorbidite` WRITE;
/*!40000 ALTER TABLE `comorbidite` DISABLE KEYS */;
INSERT INTO `comorbidite` VALUES (1,'Hypertension artérielle (HTA)','cardiovasculaire'),(2,'Diabète de type 2','métabolique'),(3,'Obésité','métabolique'),(4,'Insuffisance cardiaque','cardiovasculaire'),(5,'Fibrillation auriculaire','cardiovasculaire'),(6,'BPCO','respiratoire'),(7,'Asthme','respiratoire'),(8,'Hypothyroïdie','métabolique'),(9,'Dépression','psychiatrique'),(10,'Anxiété','psychiatrique'),(11,'Reflux gastro-oesophagien (RGO)','autre'),(12,'Syndrome métabolique','métabolique'),(13,'Insuffisance rénale chronique','autre'),(14,'Dyslipidémie','métabolique'),(15,'Accident vasculaire cérébral (AVC)','cardiovasculaire');
/*!40000 ALTER TABLE `comorbidite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation`
--

DROP TABLE IF EXISTS `consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultation` (
  `id_consultation` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_medecin` int NOT NULL,
  `date_consultation` date NOT NULL,
  `motif` varchar(255) DEFAULT NULL,
  `compte_rendu` text,
  PRIMARY KEY (`id_consultation`),
  KEY `fk_consul_medecin` (`id_medecin`),
  KEY `idx_consul_patient` (`id_patient`,`date_consultation`),
  CONSTRAINT `fk_consul_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_consul_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation`
--

LOCK TABLES `consultation` WRITE;
/*!40000 ALTER TABLE `consultation` DISABLE KEYS */;
INSERT INTO `consultation` VALUES (1,1,1,'2024-09-15','Ronflements sévères, apnées observées par conjointe, somnolence au volant','Homme 56 ans, maçon. IMC 35.8. Fumeur 15 PA. HTA sous traitement. Epworth 17/24. Tension 148/94. Suspicion SAHOS sévère. Risque professionnel conduite engins. PSG complet prescrit en urgence relative.'),(2,1,1,'2024-10-08','Bilan pré-PSG — suivi clinique jour J','Patient revu en consultation le jour de la nuit d étude. Tension 146/92. Poids 99.4kg. Somnolence diurne persistante. Pas de contre-indication. Installation PSG prévue à 21h00.'),(3,2,2,'2024-10-10','Fatigue chronique, ronflements occasionnels, céphalées matinales','Femme 44 ans, comptable. IMC 27.4. Non fumeuse. Anxiété traitée. Epworth 9/24. RGO connu. Fatigue matinale invalidante. Polygraphie ambulatoire prescrite pour éliminer SAHOS.'),(4,2,2,'2024-11-05','Bilan pré-polygraphie — suivi clinique jour J','Patiente revue en consultation le jour de l enregistrement. Poids 72.8kg. Tension 118/74. Pas de contre-indication. Installation polygraphie prévue à 22h00.');
/*!40000 ALTER TABLE `consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deces_patient`
--

DROP TABLE IF EXISTS `deces_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deces_patient` (
  `id_patient` int NOT NULL,
  `date_deces` date NOT NULL,
  `cause_principale` varchar(255) NOT NULL,
  `cause_secondaire` varchar(255) DEFAULT NULL,
  `lien_apnee` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_patient`),
  CONSTRAINT `fk_deces_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deces_patient`
--

LOCK TABLES `deces_patient` WRITE;
/*!40000 ALTER TABLE `deces_patient` DISABLE KEYS */;
/*!40000 ALTER TABLE `deces_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evenement_respiratoire`
--

DROP TABLE IF EXISTS `evenement_respiratoire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evenement_respiratoire` (
  `id_evenement` int NOT NULL AUTO_INCREMENT,
  `id_nuit` int NOT NULL,
  `type_evenement` varchar(50) NOT NULL,
  `debut_sec` int NOT NULL,
  `fin_sec` int NOT NULL,
  `duree_sec` int GENERATED ALWAYS AS ((`fin_sec` - `debut_sec`)) STORED,
  `severite` varchar(20) DEFAULT NULL,
  `decibels` decimal(5,2) DEFAULT NULL,
  `spo2_avant` decimal(5,2) DEFAULT NULL,
  `spo2_apres` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_evenement`),
  KEY `idx_evenement_nuit` (`id_nuit`),
  KEY `idx_evenement_type` (`type_evenement`),
  CONSTRAINT `fk_evenement_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `evenement_respiratoire_chk_1` CHECK ((`type_evenement` in (_utf8mb4'apnée obstructive',_utf8mb4'apnée centrale',_utf8mb4'hypopnée',_utf8mb4'RERA'))),
  CONSTRAINT `evenement_respiratoire_chk_2` CHECK ((`debut_sec` >= 0)),
  CONSTRAINT `evenement_respiratoire_chk_3` CHECK ((`severite` in (_utf8mb4'légère',_utf8mb4'modérée',_utf8mb4'sévère'))),
  CONSTRAINT `evenement_respiratoire_chk_4` CHECK ((`spo2_avant` between 0 and 100)),
  CONSTRAINT `evenement_respiratoire_chk_5` CHECK ((`spo2_apres` between 0 and 100)),
  CONSTRAINT `evenement_respiratoire_chk_6` CHECK ((`fin_sec` > `debut_sec`))
) ENGINE=InnoDB AUTO_INCREMENT=799 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evenement_respiratoire`
--

LOCK TABLES `evenement_respiratoire` WRITE;
/*!40000 ALTER TABLE `evenement_respiratoire` DISABLE KEYS */;
INSERT INTO `evenement_respiratoire` (`id_evenement`, `id_nuit`, `type_evenement`, `debut_sec`, `fin_sec`, `severite`, `decibels`, `spo2_avant`, `spo2_apres`) VALUES (455,1,'apnée obstructive',90,155,'sévère',69.80,94.80,80.00),(456,1,'apnée obstructive',162,204,'sévère',73.60,95.30,75.30),(457,1,'hypopnée',272,305,'modérée',54.40,95.50,88.70),(458,1,'apnée obstructive',323,382,'sévère',76.00,95.20,78.00),(459,1,'RERA',405,457,'légère',42.50,95.60,93.60),(460,1,'apnée obstructive',500,530,'sévère',70.40,95.10,81.30),(461,1,'apnée obstructive',604,661,'sévère',66.50,95.20,77.10),(462,1,'apnée obstructive',668,728,'sévère',69.70,94.60,78.70),(463,1,'apnée obstructive',764,823,'sévère',71.70,95.20,76.20),(464,1,'hypopnée',858,911,'modérée',54.50,95.50,87.50),(465,1,'hypopnée',951,976,'modérée',55.40,95.60,85.60),(466,1,'apnée obstructive',1033,1068,'sévère',70.60,94.70,76.80),(467,1,'RERA',1096,1142,'légère',42.00,95.70,93.70),(468,1,'apnée obstructive',1216,1254,'sévère',72.80,94.60,78.10),(469,1,'apnée obstructive',1341,1390,'sévère',69.50,95.00,79.50),(470,1,'apnée obstructive',1452,1499,'sévère',70.20,94.70,80.90),(471,1,'apnée obstructive',1543,1570,'sévère',68.00,94.80,78.40),(472,1,'apnée obstructive',1597,1656,'sévère',68.40,95.00,79.00),(473,1,'apnée obstructive',1680,1729,'sévère',75.90,94.80,81.80),(474,1,'apnée obstructive',1803,1846,'sévère',72.60,94.70,79.00),(475,1,'hypopnée',1890,1954,'modérée',58.10,95.50,85.20),(476,1,'apnée obstructive',2017,2046,'sévère',72.10,94.90,81.30),(477,1,'apnée obstructive',2139,2178,'sévère',68.90,95.20,79.20),(478,1,'hypopnée',2228,2258,'modérée',56.10,95.50,87.50),(479,1,'apnée obstructive',2289,2320,'sévère',72.80,95.10,79.60),(480,1,'apnée obstructive',2386,2440,'sévère',74.40,95.10,81.30),(481,1,'apnée obstructive',2447,2495,'sévère',72.50,94.80,78.10),(482,1,'hypopnée',2534,2581,'modérée',57.50,95.50,85.40),(483,1,'apnée centrale',2644,2686,'modérée',40.10,95.30,87.50),(484,1,'apnée obstructive',2724,2753,'sévère',67.30,95.00,81.80),(485,1,'apnée obstructive',2805,2840,'sévère',71.30,95.30,80.80),(486,1,'hypopnée',2871,2911,'modérée',55.50,95.50,86.90),(487,1,'RERA',2961,3010,'légère',46.00,95.70,92.00),(488,1,'apnée obstructive',3067,3132,'sévère',67.20,95.40,76.00),(489,1,'hypopnée',3152,3191,'modérée',59.80,95.50,87.90),(490,1,'apnée obstructive',3214,3242,'sévère',75.80,95.40,80.60),(491,1,'apnée obstructive',3328,3355,'sévère',69.70,95.20,75.10),(492,1,'apnée obstructive',3385,3435,'sévère',71.40,94.90,79.70),(493,1,'apnée obstructive',3503,3541,'sévère',72.70,95.00,80.80),(494,1,'apnée obstructive',3586,3647,'sévère',75.40,94.60,76.60),(495,1,'apnée obstructive',3731,3787,'sévère',66.30,95.30,78.90),(496,1,'apnée obstructive',3803,3857,'sévère',75.20,94.70,75.40),(497,1,'apnée centrale',3893,3926,'modérée',43.80,95.40,87.90),(498,1,'apnée obstructive',3993,4053,'sévère',70.10,94.60,81.60),(499,1,'apnée obstructive',4072,4134,'sévère',69.00,94.90,75.70),(500,1,'apnée obstructive',4155,4217,'sévère',74.90,94.60,78.20),(501,1,'apnée centrale',4270,4309,'modérée',42.70,95.30,89.80),(502,1,'apnée obstructive',4330,4363,'sévère',70.20,95.20,76.10),(503,1,'apnée obstructive',4428,4458,'sévère',70.10,94.60,78.40),(504,1,'apnée obstructive',4482,4514,'sévère',70.10,95.40,75.20),(505,1,'apnée obstructive',4599,4634,'sévère',69.70,94.90,81.70),(506,1,'apnée obstructive',4674,4726,'sévère',74.60,94.60,79.80),(507,1,'apnée obstructive',4748,4797,'sévère',71.40,95.40,77.50),(508,1,'apnée obstructive',4840,4894,'sévère',70.00,94.70,75.90),(509,1,'apnée centrale',4942,5002,'modérée',43.90,95.20,89.00),(510,1,'apnée obstructive',5017,5042,'sévère',72.40,95.00,75.10),(511,1,'hypopnée',5102,5134,'modérée',58.70,95.30,85.50),(512,1,'apnée obstructive',5191,5250,'sévère',71.60,94.60,80.40),(513,1,'apnée obstructive',5330,5382,'sévère',68.10,94.70,81.10),(514,1,'apnée obstructive',5455,5480,'sévère',69.30,94.60,81.30),(515,1,'hypopnée',5541,5582,'modérée',54.00,95.50,85.60),(516,1,'apnée obstructive',5602,5638,'sévère',67.30,94.70,76.20),(517,1,'apnée centrale',5705,5736,'modérée',42.60,95.00,87.00),(518,1,'apnée obstructive',5789,5833,'sévère',73.90,94.70,77.30),(519,1,'apnée centrale',5862,5919,'modérée',39.20,95.00,89.20),(520,1,'apnée obstructive',5935,5969,'sévère',71.30,95.20,78.30),(521,1,'RERA',6028,6063,'légère',45.90,95.60,91.30),(522,1,'apnée obstructive',6132,6190,'sévère',71.00,95.40,75.30),(523,1,'apnée obstructive',6260,6286,'sévère',73.80,95.30,78.70),(524,1,'apnée obstructive',6384,6432,'sévère',70.60,95.40,75.40),(525,1,'hypopnée',6554,6594,'modérée',56.90,95.40,87.70),(526,1,'apnée obstructive',6720,6776,'sévère',70.90,95.30,75.50),(527,1,'apnée obstructive',6802,6861,'sévère',66.80,95.00,75.50),(528,1,'apnée obstructive',6882,6915,'sévère',68.80,95.10,78.80),(529,1,'apnée obstructive',6941,7001,'sévère',69.30,95.40,78.70),(530,1,'apnée obstructive',7062,7120,'sévère',70.50,95.00,75.70),(531,1,'apnée obstructive',7152,7204,'sévère',73.00,95.30,79.60),(532,1,'apnée obstructive',7226,7285,'sévère',73.70,95.10,76.50),(533,1,'apnée obstructive',7308,7345,'sévère',70.50,94.70,77.40),(534,1,'RERA',7408,7458,'légère',44.30,95.50,91.30),(535,1,'apnée obstructive',7464,7512,'sévère',70.30,95.10,77.60),(536,1,'apnée obstructive',7550,7608,'sévère',67.50,95.30,75.50),(537,1,'apnée centrale',7623,7663,'modérée',43.80,95.00,87.30),(538,1,'hypopnée',7697,7743,'modérée',58.40,95.50,87.20),(539,1,'apnée obstructive',7793,7853,'sévère',71.90,95.00,77.30),(540,1,'apnée obstructive',7866,7905,'sévère',67.20,94.80,79.70),(541,1,'apnée obstructive',7954,8019,'sévère',73.50,95.30,80.00),(542,1,'apnée obstructive',8081,8110,'sévère',75.70,95.00,77.50),(543,1,'apnée obstructive',8124,8170,'sévère',71.80,94.70,79.60),(544,1,'apnée obstructive',8219,8259,'sévère',68.20,94.60,80.90),(545,1,'apnée obstructive',8301,8357,'sévère',69.70,95.20,79.00),(546,1,'apnée obstructive',8411,8444,'sévère',74.10,95.30,81.80),(547,1,'apnée obstructive',8489,8550,'sévère',74.20,95.10,79.50),(548,1,'apnée obstructive',8584,8624,'sévère',66.30,95.30,80.80),(549,1,'apnée obstructive',8639,8690,'sévère',68.70,94.70,79.90),(550,1,'apnée obstructive',8747,8778,'sévère',69.10,94.80,75.00),(551,1,'apnée obstructive',8820,8867,'sévère',74.70,95.00,77.80),(552,1,'hypopnée',8927,8981,'modérée',54.90,95.50,85.10),(553,1,'apnée obstructive',9002,9030,'sévère',73.50,94.70,77.90),(554,1,'apnée obstructive',9056,9087,'sévère',69.40,94.80,80.10),(555,1,'apnée obstructive',9178,9224,'sévère',73.80,95.00,75.60),(556,1,'apnée obstructive',9235,9266,'sévère',66.50,94.60,79.30),(557,1,'apnée obstructive',9335,9372,'sévère',72.70,94.70,79.60),(558,1,'apnée obstructive',9414,9447,'sévère',70.90,94.90,76.90),(559,1,'apnée obstructive',9500,9542,'sévère',73.50,94.60,78.00),(560,1,'hypopnée',9584,9613,'modérée',55.70,95.50,86.90),(561,1,'apnée obstructive',9651,9711,'sévère',72.70,94.50,77.80),(562,1,'apnée obstructive',9774,9833,'sévère',72.00,94.50,77.10),(563,1,'apnée obstructive',9863,9893,'sévère',68.10,94.60,76.80),(564,1,'RERA',9909,9949,'légère',43.60,95.30,93.20),(565,1,'apnée obstructive',10010,10066,'sévère',67.80,94.80,79.90),(566,1,'hypopnée',10116,10166,'modérée',57.00,95.50,88.20),(567,1,'apnée obstructive',10175,10210,'sévère',66.70,95.30,75.30),(568,1,'apnée centrale',10254,10303,'modérée',38.10,95.40,89.60),(569,1,'hypopnée',10339,10393,'modérée',57.50,95.40,87.80),(570,1,'apnée obstructive',10443,10503,'sévère',70.20,94.60,75.10),(571,1,'apnée obstructive',10590,10633,'sévère',69.20,95.20,79.30),(572,1,'apnée obstructive',10694,10722,'sévère',74.30,95.30,75.60),(573,1,'apnée obstructive',10752,10811,'sévère',74.40,94.70,79.10),(574,1,'apnée obstructive',10837,10882,'sévère',71.20,94.90,77.20),(575,1,'apnée obstructive',10943,11005,'sévère',69.40,94.80,76.20),(576,1,'apnée obstructive',11011,11069,'sévère',71.10,94.60,78.60),(577,1,'hypopnée',11092,11149,'modérée',59.40,95.30,87.90),(578,1,'apnée obstructive',11176,11212,'sévère',74.20,95.20,76.70),(579,1,'apnée obstructive',11292,11321,'sévère',67.50,94.70,79.20),(580,1,'apnée centrale',11363,11403,'modérée',43.30,95.30,87.50),(581,1,'apnée obstructive',11440,11501,'sévère',73.70,94.90,80.30),(582,1,'apnée obstructive',11514,11577,'sévère',73.60,94.90,81.50),(583,1,'apnée obstructive',11618,11648,'sévère',71.60,95.10,79.40),(584,1,'apnée obstructive',11710,11772,'sévère',74.60,95.10,76.10),(585,1,'apnée obstructive',11814,11859,'sévère',66.70,94.90,77.10),(586,1,'apnée obstructive',11885,11923,'sévère',68.70,94.60,78.60),(587,1,'apnée obstructive',11948,11993,'sévère',69.10,94.90,75.40),(588,1,'hypopnée',12027,12077,'modérée',59.00,95.20,88.50),(589,1,'apnée obstructive',12129,12173,'sévère',74.60,95.10,78.50),(590,1,'apnée obstructive',12191,12220,'sévère',70.60,95.00,80.50),(591,1,'apnée obstructive',12326,12390,'sévère',75.00,94.90,80.70),(592,1,'hypopnée',12471,12509,'modérée',57.90,95.30,86.90),(593,1,'apnée obstructive',12577,12610,'sévère',67.50,94.60,75.70),(594,1,'apnée obstructive',12659,12688,'sévère',75.00,94.80,80.00),(595,1,'apnée obstructive',12714,12762,'sévère',71.00,94.70,76.70),(596,1,'apnée obstructive',12826,12879,'sévère',70.40,94.90,78.70),(597,1,'apnée obstructive',12900,12944,'sévère',67.60,94.80,77.00),(598,1,'apnée obstructive',12954,13012,'sévère',70.10,94.80,79.20),(599,1,'hypopnée',13054,13114,'modérée',58.70,95.50,85.30),(600,1,'apnée obstructive',13171,13202,'sévère',66.90,95.10,77.00),(601,1,'apnée obstructive',13221,13254,'sévère',73.20,95.10,81.30),(602,1,'apnée obstructive',13330,13361,'sévère',74.70,94.80,79.10),(603,1,'hypopnée',13391,13425,'modérée',54.80,95.30,88.90),(604,1,'apnée obstructive',13473,13536,'sévère',73.00,94.90,79.20),(605,1,'RERA',13557,13603,'légère',46.70,95.50,92.10),(606,1,'hypopnée',13675,13740,'modérée',58.70,95.50,87.70),(607,1,'apnée obstructive',13806,13834,'sévère',74.30,95.20,79.80),(608,1,'apnée obstructive',13928,13980,'sévère',71.30,95.10,78.00),(609,1,'apnée obstructive',14088,14121,'sévère',69.60,94.80,76.30),(610,1,'hypopnée',14149,14190,'modérée',55.30,95.60,86.90),(611,1,'apnée obstructive',14254,14307,'sévère',68.30,94.60,75.50),(612,1,'apnée obstructive',14339,14391,'sévère',74.40,94.60,80.40),(613,1,'hypopnée',14399,14431,'modérée',59.00,95.60,85.20),(614,1,'apnée obstructive',14508,14542,'sévère',69.40,95.20,75.90),(615,1,'RERA',14594,14642,'légère',43.90,95.40,93.50),(616,1,'apnée obstructive',14671,14705,'sévère',73.70,95.20,76.20),(617,1,'apnée obstructive',14750,14777,'sévère',70.40,94.90,79.70),(618,1,'apnée obstructive',14865,14892,'sévère',68.40,94.90,77.00),(619,1,'apnée obstructive',14939,14977,'sévère',73.50,94.90,78.70),(620,1,'apnée obstructive',15007,15038,'sévère',69.10,95.20,78.30),(621,1,'apnée obstructive',15118,15178,'sévère',74.40,94.80,81.60),(622,1,'apnée obstructive',15208,15259,'sévère',75.80,94.90,77.00),(623,1,'apnée obstructive',15290,15324,'sévère',69.80,95.00,81.80),(624,1,'apnée obstructive',15372,15412,'sévère',74.20,95.20,76.00),(625,1,'apnée obstructive',15457,15493,'sévère',68.50,95.10,81.10),(626,1,'apnée obstructive',15507,15533,'sévère',71.50,94.60,80.90),(627,1,'hypopnée',15622,15668,'modérée',59.10,95.30,88.10),(628,1,'apnée obstructive',15708,15759,'sévère',68.70,95.30,76.00),(629,1,'apnée obstructive',15765,15805,'sévère',70.40,95.40,76.60),(630,1,'apnée obstructive',15856,15887,'sévère',70.50,94.80,75.20),(631,1,'apnée obstructive',15965,15992,'sévère',66.50,95.00,76.70),(632,1,'apnée obstructive',16016,16055,'sévère',75.90,94.80,75.20),(633,1,'apnée obstructive',16109,16163,'sévère',75.30,95.30,79.50),(634,1,'apnée obstructive',16187,16226,'sévère',73.90,94.60,77.00),(635,1,'hypopnée',16281,16318,'modérée',59.00,95.50,85.60),(636,1,'apnée obstructive',16389,16431,'sévère',73.10,94.90,75.00),(637,1,'apnée centrale',16448,16490,'modérée',38.60,95.10,89.50),(638,1,'RERA',16535,16592,'légère',44.70,95.70,92.60),(639,1,'apnée obstructive',16617,16676,'sévère',67.10,94.80,77.10),(640,1,'apnée obstructive',16690,16716,'sévère',66.50,94.90,80.60),(641,1,'apnée obstructive',16778,16819,'sévère',70.60,94.60,81.30),(642,1,'apnée obstructive',16856,16897,'sévère',72.00,94.50,78.60),(643,1,'apnée obstructive',16961,17024,'sévère',68.40,94.60,78.00),(644,1,'apnée obstructive',17046,17091,'sévère',72.10,94.70,77.90),(645,1,'apnée obstructive',17114,17171,'sévère',72.60,94.60,81.80),(646,1,'apnée obstructive',17203,17264,'sévère',66.70,95.00,78.60),(647,1,'apnée obstructive',17314,17341,'sévère',75.90,95.00,77.70),(648,1,'apnée obstructive',17389,17414,'sévère',70.70,95.10,81.90),(649,1,'apnée obstructive',17483,17542,'sévère',68.50,94.50,80.50),(650,1,'apnée obstructive',17551,17588,'sévère',69.40,95.20,79.40),(651,1,'apnée obstructive',17666,17695,'sévère',73.70,95.20,77.30),(652,1,'apnée obstructive',17734,17780,'sévère',66.40,95.00,80.70),(653,1,'apnée obstructive',17824,17856,'sévère',67.80,95.20,78.30),(654,1,'apnée obstructive',17898,17942,'sévère',73.00,95.10,80.70),(655,1,'apnée obstructive',17973,18024,'sévère',66.60,95.20,78.20),(656,1,'apnée obstructive',18070,18113,'sévère',68.90,94.50,76.40),(657,1,'apnée obstructive',18147,18184,'sévère',66.40,95.30,78.60),(658,1,'apnée centrale',18245,18294,'modérée',44.90,95.20,87.80),(659,1,'hypopnée',18327,18363,'modérée',58.50,95.30,86.40),(660,1,'apnée obstructive',18401,18445,'sévère',73.80,95.30,77.30),(661,1,'apnée obstructive',18481,18506,'sévère',67.20,94.80,81.20),(662,1,'apnée obstructive',18572,18610,'sévère',73.40,95.30,77.70),(663,1,'apnée obstructive',18666,18728,'sévère',75.70,94.90,78.50),(664,1,'apnée obstructive',18743,18788,'sévère',75.20,95.00,80.60),(665,1,'apnée obstructive',18839,18892,'sévère',73.30,94.60,79.20),(666,1,'apnée obstructive',18913,18970,'sévère',74.20,95.00,77.20),(667,1,'apnée obstructive',19008,19043,'sévère',66.80,95.10,77.10),(668,1,'apnée obstructive',19085,19128,'sévère',72.00,94.90,79.80),(669,1,'RERA',19175,19240,'légère',43.80,95.30,93.60),(670,1,'apnée obstructive',19270,19300,'sévère',69.50,95.40,76.90),(671,1,'apnée obstructive',19347,19387,'sévère',75.80,95.40,75.50),(672,1,'apnée obstructive',19439,19478,'sévère',72.40,94.80,80.60),(673,1,'apnée centrale',19484,19518,'modérée',42.80,95.40,87.40),(674,1,'apnée obstructive',19618,19658,'sévère',72.10,95.20,75.20),(675,1,'RERA',19696,19760,'légère',42.30,95.70,92.10),(676,1,'apnée obstructive',19851,19916,'sévère',69.80,95.00,79.20),(677,1,'apnée obstructive',19932,19981,'sévère',72.80,95.40,77.60),(678,1,'apnée obstructive',19999,20039,'sévère',73.60,95.00,78.70),(679,1,'apnée obstructive',20122,20147,'sévère',70.00,95.10,76.70),(680,1,'apnée obstructive',20201,20232,'sévère',67.10,95.20,78.50),(681,1,'apnée obstructive',20255,20294,'sévère',69.90,95.00,76.80),(682,1,'apnée obstructive',20354,20412,'sévère',68.60,94.90,82.00),(683,1,'apnée obstructive',20428,20488,'sévère',68.90,95.30,78.40),(684,1,'apnée obstructive',20524,20556,'sévère',67.20,95.30,78.20),(685,1,'apnée centrale',20619,20673,'modérée',44.30,95.20,87.30),(686,1,'apnée obstructive',20700,20760,'sévère',72.80,95.30,77.20),(687,1,'apnée centrale',20786,20839,'modérée',40.40,95.00,88.60),(688,1,'hypopnée',20861,20918,'modérée',59.30,95.50,87.80),(689,1,'apnée obstructive',20947,21007,'sévère',75.30,95.10,80.60),(690,1,'RERA',21047,21082,'légère',44.50,95.40,91.60),(691,1,'apnée obstructive',21117,21172,'sévère',67.40,95.20,75.20),(692,1,'apnée centrale',21221,21261,'modérée',41.90,95.10,89.40),(693,1,'apnée obstructive',21303,21345,'sévère',71.50,95.10,75.60),(694,1,'apnée obstructive',21373,21431,'sévère',69.10,95.40,80.00),(695,1,'apnée centrale',21447,21487,'modérée',41.70,95.30,89.50),(696,1,'apnée obstructive',21554,21583,'sévère',66.70,95.40,79.50),(697,1,'apnée obstructive',21617,21657,'sévère',70.50,95.10,77.40),(698,1,'apnée obstructive',21733,21778,'sévère',74.80,95.20,79.50),(699,1,'apnée obstructive',21877,21916,'sévère',67.80,95.40,78.00),(700,1,'apnée obstructive',21978,22012,'sévère',75.10,94.50,75.90),(701,1,'apnée obstructive',22048,22077,'sévère',67.50,94.60,77.30),(702,1,'apnée obstructive',22139,22185,'sévère',73.10,94.80,81.60),(703,1,'apnée obstructive',22199,22250,'sévère',74.90,95.30,76.80),(704,1,'apnée obstructive',22301,22352,'sévère',72.40,95.00,75.90),(705,1,'apnée obstructive',22414,22476,'sévère',69.00,95.00,78.50),(706,1,'hypopnée',22494,22520,'modérée',55.00,95.60,85.60),(707,1,'apnée obstructive',22555,22616,'sévère',72.60,95.10,79.20),(708,1,'apnée obstructive',22668,22693,'sévère',74.40,95.00,80.80),(709,1,'apnée obstructive',22743,22787,'sévère',66.30,94.50,79.50),(710,1,'apnée obstructive',22817,22868,'sévère',71.80,95.10,80.40),(711,1,'apnée obstructive',22915,22974,'sévère',70.20,95.10,78.50),(712,1,'apnée obstructive',22984,23023,'sévère',72.30,94.80,81.70),(713,1,'hypopnée',23066,23108,'modérée',56.90,95.50,87.70),(714,1,'apnée obstructive',23149,23175,'sévère',69.00,94.60,75.40),(715,1,'hypopnée',23251,23301,'modérée',56.60,95.40,85.80),(716,1,'apnée obstructive',23345,23399,'sévère',72.10,94.80,80.00),(717,1,'apnée obstructive',23411,23475,'sévère',73.30,95.30,81.80),(718,1,'hypopnée',23498,23548,'modérée',54.80,95.30,87.20),(719,1,'apnée obstructive',23557,23583,'sévère',69.20,94.90,76.90),(720,1,'apnée obstructive',23645,23697,'sévère',68.50,94.60,77.00),(721,1,'apnée centrale',23732,23786,'modérée',40.70,95.20,87.70),(722,1,'apnée obstructive',23827,23868,'sévère',74.70,94.60,77.30),(723,1,'apnée centrale',23915,23953,'modérée',42.00,95.10,89.30),(724,1,'apnée obstructive',24016,24062,'sévère',71.00,95.00,78.50),(725,1,'apnée obstructive',24076,24125,'sévère',69.10,94.50,81.60),(726,1,'apnée obstructive',24159,24210,'sévère',71.10,95.40,76.50),(727,1,'apnée obstructive',24255,24285,'sévère',69.50,94.50,78.50),(728,1,'apnée obstructive',24319,24378,'sévère',74.80,95.10,78.30),(729,1,'apnée centrale',24412,24459,'modérée',41.80,95.30,88.30),(730,1,'apnée obstructive',24526,24555,'sévère',74.80,95.20,80.30),(731,1,'apnée obstructive',24609,24636,'sévère',69.70,94.90,79.00),(732,1,'apnée obstructive',24666,24706,'sévère',67.90,95.00,75.50),(733,1,'apnée obstructive',24772,24798,'sévère',71.00,95.20,77.00),(734,1,'apnée obstructive',24831,24871,'sévère',75.90,95.10,75.80),(735,1,'apnée obstructive',24938,24970,'sévère',75.80,94.90,80.60),(736,2,'hypopnée',90,114,'légère',44.00,97.50,91.40),(737,2,'hypopnée',563,586,'légère',43.20,97.30,90.30),(738,2,'hypopnée',867,883,'légère',42.30,97.10,89.50),(739,2,'hypopnée',1322,1341,'légère',44.80,97.20,90.70),(740,2,'hypopnée',1650,1673,'légère',45.10,97.20,90.80),(741,2,'hypopnée',2069,2085,'légère',43.00,97.50,91.30),(742,2,'hypopnée',2450,2469,'légère',43.80,97.20,91.70),(743,2,'hypopnée',2751,2772,'légère',45.20,97.40,89.30),(744,2,'hypopnée',3311,3329,'légère',46.90,97.20,91.00),(745,2,'hypopnée',3592,3613,'légère',47.90,97.30,91.60),(746,2,'hypopnée',3983,3996,'légère',46.40,97.30,88.10),(747,2,'RERA',4523,4545,'légère',38.90,97.70,95.60),(748,2,'hypopnée',4859,4880,'légère',46.70,97.30,91.20),(749,2,'hypopnée',5353,5365,'légère',45.50,97.10,90.80),(750,2,'hypopnée',5706,5728,'légère',45.70,97.40,88.70),(751,2,'hypopnée',5917,5938,'légère',46.10,97.00,92.30),(752,2,'hypopnée',6344,6368,'légère',42.70,97.00,89.40),(753,2,'RERA',6853,6873,'légère',37.60,97.60,94.80),(754,2,'hypopnée',7137,7153,'légère',46.60,97.50,91.90),(755,2,'hypopnée',7593,7614,'légère',46.40,97.00,88.60),(756,2,'hypopnée',8002,8027,'légère',43.20,97.20,91.00),(757,2,'hypopnée',8393,8406,'légère',45.20,97.20,88.80),(758,2,'RERA',8756,8774,'légère',40.60,97.40,94.70),(759,2,'hypopnée',9098,9120,'légère',46.60,97.40,90.90),(760,2,'hypopnée',9547,9561,'légère',46.20,97.30,88.90),(761,2,'hypopnée',9982,10005,'légère',43.50,97.30,89.00),(762,2,'RERA',10484,10506,'légère',40.90,97.40,94.60),(763,2,'hypopnée',10836,10861,'légère',43.20,97.40,89.40),(764,2,'RERA',11159,11171,'légère',38.40,97.70,95.60),(765,2,'hypopnée',11507,11524,'légère',43.60,97.10,91.00),(766,2,'hypopnée',12073,12086,'légère',44.30,97.50,91.70),(767,2,'hypopnée',12444,12462,'légère',47.70,97.40,89.30),(768,2,'hypopnée',12869,12894,'légère',43.70,97.40,89.60),(769,2,'hypopnée',13236,13258,'légère',44.70,97.10,90.20),(770,2,'hypopnée',13524,13543,'légère',43.20,97.30,92.20),(771,2,'hypopnée',13944,13959,'légère',46.20,97.10,90.80),(772,2,'hypopnée',14397,14418,'légère',45.50,97.10,91.00),(773,2,'hypopnée',14718,14740,'légère',45.20,97.30,88.20),(774,2,'hypopnée',15057,15069,'légère',44.50,97.40,88.50),(775,2,'hypopnée',15435,15455,'légère',46.60,97.00,90.50),(776,2,'hypopnée',15904,15920,'légère',47.60,97.20,92.20),(777,2,'hypopnée',16311,16334,'légère',47.30,97.20,88.90),(778,2,'hypopnée',16822,16834,'légère',47.80,97.20,90.90),(779,2,'hypopnée',17177,17198,'légère',47.40,97.00,90.60),(780,2,'hypopnée',17420,17443,'légère',45.20,97.40,92.20),(781,2,'hypopnée',17782,17802,'légère',47.50,97.10,92.00),(782,2,'RERA',18196,18214,'légère',37.70,97.70,96.00),(783,2,'hypopnée',18787,18812,'légère',44.40,97.20,92.20),(784,2,'hypopnée',19190,19209,'légère',47.80,97.50,91.90),(785,2,'hypopnée',19559,19581,'légère',42.10,97.30,88.50),(786,2,'hypopnée',19978,19997,'légère',47.90,97.10,92.50),(787,2,'hypopnée',20274,20290,'légère',45.30,97.20,92.20),(788,2,'hypopnée',20647,20663,'légère',47.10,97.20,88.90),(789,2,'hypopnée',21177,21196,'légère',42.70,97.10,90.10),(790,2,'hypopnée',21448,21463,'légère',43.50,97.10,91.30),(791,2,'hypopnée',21827,21841,'légère',46.70,97.30,91.40),(792,2,'RERA',22252,22273,'légère',37.70,97.60,95.80),(793,2,'hypopnée',22732,22746,'légère',47.00,97.30,88.40),(794,2,'hypopnée',23106,23122,'légère',46.00,97.10,88.60),(795,2,'hypopnée',23417,23442,'légère',43.90,97.10,89.20),(796,2,'hypopnée',23835,23859,'légère',43.40,97.40,92.30),(797,2,'RERA',24110,24135,'légère',38.20,97.60,94.00),(798,2,'hypopnée',24576,24599,'légère',45.90,97.30,88.30);
/*!40000 ALTER TABLE `evenement_respiratoire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infirmier`
--

DROP TABLE IF EXISTS `infirmier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `infirmier` (
  `id_personnel` int NOT NULL,
  `diplome` varchar(100) DEFAULT NULL,
  `experience_ans` int DEFAULT NULL,
  PRIMARY KEY (`id_personnel`),
  CONSTRAINT `fk_infirmier_personnel` FOREIGN KEY (`id_personnel`) REFERENCES `personnel` (`id_personnel`),
  CONSTRAINT `infirmier_chk_1` CHECK ((`experience_ans` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infirmier`
--

LOCK TABLES `infirmier` WRITE;
/*!40000 ALTER TABLE `infirmier` DISABLE KEYS */;
INSERT INTO `infirmier` VALUES (8,'IDE',8),(9,'IDE',7),(10,'IDE',6),(11,'IDE',5),(12,'IDE',4),(13,'IDE',3),(14,'IDE',2),(15,'IDE',1);
/*!40000 ALTER TABLE `infirmier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medecin`
--

DROP TABLE IF EXISTS `medecin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medecin` (
  `id_personnel` int NOT NULL,
  `specialite` varchar(100) NOT NULL,
  `numero_rpps` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_personnel`),
  UNIQUE KEY `numero_rpps` (`numero_rpps`),
  CONSTRAINT `fk_medecin_personnel` FOREIGN KEY (`id_personnel`) REFERENCES `personnel` (`id_personnel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medecin`
--

LOCK TABLES `medecin` WRITE;
/*!40000 ALTER TABLE `medecin` DISABLE KEYS */;
INSERT INTO `medecin` VALUES (1,'Médecine du sommeil','RPPS10011001'),(2,'Médecine du sommeil','RPPS10022002'),(3,'Médecine du sommeil','RPPS10033003'),(4,'Médecine du sommeil','RPPS10044004'),(5,'Pneumologie','RPPS10055005'),(6,'Cardiologie','RPPS10066006'),(7,'Endocrinologie','RPPS10077007');
/*!40000 ALTER TABLE `medecin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nuit_etude`
--

DROP TABLE IF EXISTS `nuit_etude`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nuit_etude` (
  `id_nuit` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_superviseur` int NOT NULL COMMENT 'Infirmier superviseur',
  `id_medecin` int NOT NULL,
  `id_appareil_psg` int NOT NULL,
  `date_nuit` date NOT NULL,
  `type_etude` varchar(50) NOT NULL,
  `notes_techniques` text,
  PRIMARY KEY (`id_nuit`),
  KEY `fk_nuit_superviseur` (`id_superviseur`),
  KEY `fk_nuit_medecin` (`id_medecin`),
  KEY `fk_nuit_appareil_psg` (`id_appareil_psg`),
  KEY `idx_nuit_patient` (`id_patient`,`date_nuit`),
  CONSTRAINT `fk_nuit_appareil_psg` FOREIGN KEY (`id_appareil_psg`) REFERENCES `appareil_psg` (`id_appareil`),
  CONSTRAINT `fk_nuit_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_nuit_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `fk_nuit_superviseur` FOREIGN KEY (`id_superviseur`) REFERENCES `infirmier` (`id_personnel`),
  CONSTRAINT `nuit_etude_chk_1` CHECK ((`type_etude` in (_utf8mb4'polysomnographie',_utf8mb4'polygraphie',_utf8mb4'titration CPAP')))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nuit_etude`
--

LOCK TABLES `nuit_etude` WRITE;
/*!40000 ALTER TABLE `nuit_etude` DISABLE KEYS */;
INSERT INTO `nuit_etude` VALUES (1,1,8,1,1,'2024-10-08','polysomnographie','Installation 21h00. Patient coopérant malgré appréhension. Calibration capteurs 21h45. Endormissement 22h12. Ronflements très intenses dès onset sommeil. Recalibration SpO2 à 01h30. Réveil naturel 06h28. Signal complet 7h16 exploitable. Fichier brut : signal_psg_patient_severe.csv'),(2,2,9,2,4,'2024-11-05','polygraphie','Enregistrement ambulatoire posé en consultation à 17h30. Patiente rentrée à domicile. Démarrage automatique 22h00. Latence endormissement estimée 38 min. Signal de bonne qualité. Retour appareil le lendemain matin. Fichier brut : signal_psg_patient_leger.csv');
/*!40000 ALTER TABLE `nuit_etude` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id_patient` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_naissance` date NOT NULL,
  `sexe` char(1) NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `numero_secu` varchar(20) DEFAULT NULL,
  `imc_initial` decimal(4,1) DEFAULT NULL,
  `fumeur` tinyint(1) DEFAULT '0',
  `pa_tabac` int DEFAULT NULL COMMENT 'Paquets-années au diagnostic',
  `consommation_alcool` varchar(50) DEFAULT NULL COMMENT 'aucune / occasionnelle / régulière / excessive',
  `profession` varchar(100) DEFAULT NULL,
  `niveau_activite` varchar(50) DEFAULT NULL COMMENT 'sédentaire / modéré / actif',
  `date_creation_dpi` date NOT NULL DEFAULT (curdate()),
  `actif` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_patient`),
  UNIQUE KEY `numero_secu` (`numero_secu`),
  CONSTRAINT `patient_chk_1` CHECK ((`sexe` in (_utf8mb4'M',_utf8mb4'F')))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'Tessier','Bernard','1968-07-15','M','3 rue des Tonneliers, Arles','0611445588','bernard.tessier@gmail.com','1 68 07 13 058 114',35.8,1,15,'occasionnelle','Maçon','modéré','2024-09-10',1),(2,'Vernet','Isabelle','1980-03-28','F','14 allée des Platanes, Tarascon','0622556699','isabelle.vernet@sfr.fr','2 80 03 13 142 225',27.4,0,0,'aucune','Comptable','modéré','2024-10-05',1);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_comorbidite`
--

DROP TABLE IF EXISTS `patient_comorbidite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_comorbidite` (
  `id_patient` int NOT NULL,
  `id_comorbidite` int NOT NULL,
  `date_diagnostic` date DEFAULT NULL,
  PRIMARY KEY (`id_patient`,`id_comorbidite`),
  KEY `fk_pc_comorbidite` (`id_comorbidite`),
  CONSTRAINT `fk_pc_comorbidite` FOREIGN KEY (`id_comorbidite`) REFERENCES `comorbidite` (`id_comorbidite`),
  CONSTRAINT `fk_pc_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_comorbidite`
--

LOCK TABLES `patient_comorbidite` WRITE;
/*!40000 ALTER TABLE `patient_comorbidite` DISABLE KEYS */;
INSERT INTO `patient_comorbidite` VALUES (1,1,'2019-04-12'),(1,3,'2020-08-20'),(1,14,'2021-03-15'),(2,10,'2022-06-18'),(2,11,'2023-09-22');
/*!40000 ALTER TABLE `patient_comorbidite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel`
--

DROP TABLE IF EXISTS `personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel` (
  `id_personnel` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_embauche` date DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_personnel`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel`
--

LOCK TABLES `personnel` WRITE;
/*!40000 ALTER TABLE `personnel` DISABLE KEYS */;
INSERT INTO `personnel` VALUES (1,'Estri','Thomas','2015-09-01','0611223344','thomas.estrii@clinique-sommeil-arles.fr',1),(2,'Faure','Isabelle','2017-03-15','0622334455','isabelle.faure@clinique-sommeil-arles.fr',1),(3,'Nakamura','Kenji','2019-06-01','0633445566','kenji.nakamura@clinique-sommeil-arles.fr',1),(4,'Bencherif','Samia','2020-01-10','0644556677','samia.bencherif@clinique-sommeil-arles.fr',1),(5,'Garnier','Laurent','2016-04-01','0655667788','laurent.garnier@clinique-sommeil-arles.fr',1),(6,'Moreau','Claire','2018-09-01','0666778899','claire.moreau@clinique-sommeil-arles.fr',1),(7,'Dupuis','Marc','2021-02-01','0677889900','marc.dupuis@clinique-sommeil-arles.fr',1),(8,'Roux','Nathalie','2016-01-01','0688990011','nathalie.roux@clinique-sommeil-arles.fr',1),(9,'Martin','Sophie','2017-06-01','0699001122','sophie.martin@clinique-sommeil-arles.fr',1),(10,'Bernard','Céline','2018-03-01','0611223355','celine.bernard@clinique-sommeil-arles.fr',1),(11,'Petit','Aurélie','2019-09-01','0622334466','aurelie.petit@clinique-sommeil-arles.fr',1),(12,'Leroy','Marine','2020-04-01','0633445577','marine.leroy@clinique-sommeil-arles.fr',1),(13,'Simon','Julie','2021-01-01','0644556688','julie.simon@clinique-sommeil-arles.fr',1),(14,'Michel','Fatima','2022-06-01','0655667799','fatima.michel@clinique-sommeil-arles.fr',1),(15,'Lefebvre','Amandine','2023-01-01','0666778800','amandine.lefebvre@clinique-sommeil-arles.fr',1);
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription_nuit`
--

DROP TABLE IF EXISTS `prescription_nuit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription_nuit` (
  `id_prescription` int NOT NULL AUTO_INCREMENT,
  `id_consultation` int NOT NULL,
  `id_nuit` int DEFAULT NULL,
  `motif_prescription` varchar(255) DEFAULT NULL,
  `urgence` varchar(20) NOT NULL DEFAULT 'normale',
  PRIMARY KEY (`id_prescription`),
  KEY `fk_prescription_consul` (`id_consultation`),
  KEY `fk_prescription_nuit` (`id_nuit`),
  CONSTRAINT `fk_prescription_consul` FOREIGN KEY (`id_consultation`) REFERENCES `consultation` (`id_consultation`),
  CONSTRAINT `fk_prescription_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `prescription_nuit_chk_1` CHECK ((`urgence` in (_utf8mb4'normale',_utf8mb4'urgente')))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription_nuit`
--

LOCK TABLES `prescription_nuit` WRITE;
/*!40000 ALTER TABLE `prescription_nuit` DISABLE KEYS */;
INSERT INTO `prescription_nuit` VALUES (1,2,1,'Suspicion SAHOS sévère — risque professionnel conduite','urgente'),(2,4,2,'Suspicion SAHOS léger — fatigue chronique invalidante','normale');
/*!40000 ALTER TABLE `prescription_nuit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resultat_nuit`
--

DROP TABLE IF EXISTS `resultat_nuit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultat_nuit` (
  `id_resultat` int NOT NULL AUTO_INCREMENT,
  `id_nuit` int NOT NULL,
  `id_medecin_validateur` int NOT NULL,
  `date_validation` date NOT NULL,
  `iah` decimal(5,2) DEFAULT NULL COMMENT 'Index Apnée-Hypopnée — événements/heure',
  `spo2_min` decimal(5,2) DEFAULT NULL,
  `spo2_moy` decimal(5,2) DEFAULT NULL,
  `spo2_mediane` decimal(5,2) DEFAULT NULL,
  `nb_apnees` int DEFAULT NULL,
  `nb_hypopnees` int DEFAULT NULL,
  `nb_rera` int DEFAULT NULL,
  `nb_microeveils` int DEFAULT NULL,
  `duree_sommeil_min` int DEFAULT NULL,
  `duree_hypoxie_min` int DEFAULT NULL,
  `position_dominante` varchar(20) DEFAULT NULL,
  `duree_apnee_moy_sec` int DEFAULT NULL,
  `duree_apnee_max_sec` int DEFAULT NULL,
  `decibels_max` decimal(5,2) DEFAULT NULL,
  `decibels_moy` decimal(5,2) DEFAULT NULL,
  `nb_ronflements_forts` int DEFAULT NULL,
  `severite_iah` varchar(20) GENERATED ALWAYS AS ((case when (`iah` < 5) then _utf8mb4'normal' when (`iah` < 15) then _utf8mb4'léger' when (`iah` < 30) then _utf8mb4'modéré' else _utf8mb4'sévère' end)) STORED,
  `commentaire_medical` text,
  PRIMARY KEY (`id_resultat`),
  UNIQUE KEY `id_nuit` (`id_nuit`),
  KEY `fk_resultat_medecin` (`id_medecin_validateur`),
  KEY `idx_resultat_iah` (`iah`),
  CONSTRAINT `fk_resultat_medecin` FOREIGN KEY (`id_medecin_validateur`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_resultat_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `resultat_nuit_chk_1` CHECK ((`iah` >= 0)),
  CONSTRAINT `resultat_nuit_chk_10` CHECK ((`duree_hypoxie_min` >= 0)),
  CONSTRAINT `resultat_nuit_chk_11` CHECK ((`position_dominante` in (_utf8mb4'dorsale',_utf8mb4'latérale',_utf8mb4'ventrale',_utf8mb4'mixte'))),
  CONSTRAINT `resultat_nuit_chk_12` CHECK ((`duree_apnee_moy_sec` >= 0)),
  CONSTRAINT `resultat_nuit_chk_13` CHECK ((`duree_apnee_max_sec` >= 0)),
  CONSTRAINT `resultat_nuit_chk_14` CHECK ((`nb_ronflements_forts` >= 0)),
  CONSTRAINT `resultat_nuit_chk_2` CHECK ((`spo2_min` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_3` CHECK ((`spo2_moy` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_4` CHECK ((`spo2_mediane` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_5` CHECK ((`nb_apnees` >= 0)),
  CONSTRAINT `resultat_nuit_chk_6` CHECK ((`nb_hypopnees` >= 0)),
  CONSTRAINT `resultat_nuit_chk_7` CHECK ((`nb_rera` >= 0)),
  CONSTRAINT `resultat_nuit_chk_8` CHECK ((`nb_microeveils` >= 0)),
  CONSTRAINT `resultat_nuit_chk_9` CHECK ((`duree_sommeil_min` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultat_nuit`
--

LOCK TABLES `resultat_nuit` WRITE;
/*!40000 ALTER TABLE `resultat_nuit` DISABLE KEYS */;
/*!40000 ALTER TABLE `resultat_nuit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suivi_cpap_jour`
--

DROP TABLE IF EXISTS `suivi_cpap_jour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suivi_cpap_jour` (
  `id_suivi` int NOT NULL AUTO_INCREMENT,
  `id_appareil` int NOT NULL,
  `date_jour` date NOT NULL,
  `duree_utilisation_h` decimal(4,2) DEFAULT NULL,
  `iah_residuel` decimal(5,2) DEFAULT NULL,
  `fuites_l_min` decimal(6,2) DEFAULT NULL,
  `nb_evenements` int DEFAULT NULL,
  `qualite_donnee` varchar(20) NOT NULL DEFAULT 'bonne',
  PRIMARY KEY (`id_suivi`),
  UNIQUE KEY `id_appareil` (`id_appareil`,`date_jour`),
  KEY `idx_suivi_cpap_date` (`date_jour`),
  KEY `idx_suivi_cpap_appareil` (`id_appareil`,`date_jour`),
  CONSTRAINT `fk_suivi_cpap_appareil` FOREIGN KEY (`id_appareil`) REFERENCES `appareil_cpap` (`id_appareil`),
  CONSTRAINT `suivi_cpap_jour_chk_1` CHECK ((`duree_utilisation_h` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_2` CHECK ((`iah_residuel` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_3` CHECK ((`fuites_l_min` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_4` CHECK ((`nb_evenements` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_5` CHECK ((`qualite_donnee` in (_utf8mb4'bonne',_utf8mb4'dégradée',_utf8mb4'manquante')))
) ENGINE=InnoDB AUTO_INCREMENT=442 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suivi_cpap_jour`
--

LOCK TABLES `suivi_cpap_jour` WRITE;
/*!40000 ALTER TABLE `suivi_cpap_jour` DISABLE KEYS */;
/*!40000 ALTER TABLE `suivi_cpap_jour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suivi_patient`
--

DROP TABLE IF EXISTS `suivi_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suivi_patient` (
  `id_suivi` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_medecin` int NOT NULL,
  `date_suivi` date NOT NULL,
  `poids` decimal(5,2) DEFAULT NULL,
  `imc` decimal(4,1) DEFAULT NULL,
  `tension_systolique` int DEFAULT NULL,
  `tension_diastolique` int DEFAULT NULL,
  `statut_tabac` varchar(50) DEFAULT NULL COMMENT 'fumeur / sevrage en cours / arrêté / non-fumeur',
  `notes_evolution` text,
  `statut_patient` varchar(20) NOT NULL DEFAULT 'actif',
  PRIMARY KEY (`id_suivi`),
  KEY `fk_suivi_patient_patient` (`id_patient`),
  KEY `fk_suivi_patient_medecin` (`id_medecin`),
  CONSTRAINT `fk_suivi_patient_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_suivi_patient_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `suivi_patient_chk_1` CHECK ((`statut_patient` in (_utf8mb4'actif',_utf8mb4'perdu de vue',_utf8mb4'décédé')))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suivi_patient`
--

LOCK TABLES `suivi_patient` WRITE;
/*!40000 ALTER TABLE `suivi_patient` DISABLE KEYS */;
INSERT INTO `suivi_patient` VALUES (15,1,1,'2024-10-08',99.40,35.6,146,92,'fumeur','Bilan pré-PSG. Somnolence sévère Epworth 17/24. HTA mal contrôlée. Patient informé du déroulement de la nuit. Arrêt tabac recommandé.','actif'),(16,2,2,'2024-11-05',72.80,27.4,118,74,'non-fumeur','Bilan pré-polygraphie. Fatigue matinale. Anxiété stable sous traitement. Patiente coopérante. Pas de contre-indication.','actif');
/*!40000 ALTER TABLE `suivi_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'cliniquev3'
--

--
-- Dumping routines for database 'cliniquev3'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_creer_resultat_nuit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_creer_resultat_nuit`(
    IN p_id_nuit INT,
    IN p_spo2_min DECIMAL(5,2),
    IN p_spo2_moy DECIMAL(5,2),
    IN p_spo2_mediane DECIMAL(5,2),
    IN p_duree_hypoxie_min DECIMAL(6,2),
    IN p_position_dominante VARCHAR(20),
    IN p_decibels_max DECIMAL(5,2),
    IN p_decibels_moy DECIMAL(5,2),
    IN p_nb_ronflements_forts INT
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
        WHEN LOWER(p_position_dominante) LIKE '%lat%' THEN 'latérale'
        WHEN LOWER(p_position_dominante) LIKE '%vent%' THEN 'ventrale'
        ELSE 'mixte'
    END;

    -- Récupération complète depuis evenement_respiratoire
SELECT
    COUNT(CASE WHEN type_evenement LIKE '%apnée%' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'hypopnée' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'RERA' THEN 1 END),
    ROUND(AVG(duree_sec), 0),
    MAX(duree_sec)
INTO v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_duree_apnee_moy, v_duree_apnee_max
FROM evenement_respiratoire
WHERE id_nuit = p_id_nuit;

-- AJOUT NÉCESSAIRE : extrapolation 2h → 7h (×3.5)
SET v_nb_apnees    = ROUND(v_nb_apnees * 3.5);
SET v_nb_hypopnees = ROUND(v_nb_hypopnees * 3.5);
SET v_nb_rera        = ROUND(v_nb_rera * 3.5);

-- Micro-éveils : maintenant calculé depuis les valeurs déjà extrapolées
SET v_nb_microeveils = v_nb_apnees + v_nb_hypopnees + v_nb_rera;
    -- Insertion avec extrapolation 2h → 7h
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
        1,
        CURDATE(),
        p_spo2_min, p_spo2_moy, p_spo2_mediane,
        p_duree_hypoxie_min, v_position,
        p_decibels_max, p_decibels_moy, p_nb_ronflements_forts,
        v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_nb_microeveils,
        v_duree_apnee_moy, v_duree_apnee_max,
        ROUND((v_nb_apnees + v_nb_hypopnees)/7, 2),   -- 
        420
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
           ROUND((v_nb_apnees + v_nb_hypopnees) /7, 2) AS iah;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_lire_resultat_nuit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_lire_resultat_nuit`(
    IN  p_id_nuit  INT
)
BEGIN
 
    -- Une seule requête qui rassemble tout ce dont le rapport
    -- a besoin : identité patient, infos nuit, et résultat complet.
    -- Le rapport Python n'a donc qu'un seul appel à faire,
    -- pas de jointures à gérer côté Python.
    SELECT
        -- Identité patient
        p.id_patient,
        p.nom,
        p.prenom,
 
        -- Contexte de la nuit
        n.id_nuit,
        n.date_nuit,
        n.type_etude,
 
        -- Médecin qui a validé le résultat
        m.id_personnel   AS id_medecin,
        per.nom          AS nom_medecin,
        per.prenom       AS prenom_medecin,
 
        -- Résultat complet de la nuit
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
        r.duree_apnee_moy_sec,
        r.duree_apnee_max_sec,
        r.decibels_max,
        r.decibels_moy,
        r.nb_ronflements_forts,
        r.commentaire_medical,
        r.date_validation
 
    FROM resultat_nuit r
    JOIN nuit_etude n        ON n.id_nuit = r.id_nuit
    JOIN patient p           ON p.id_patient = n.id_patient
    JOIN medecin m            ON m.id_personnel = r.id_medecin_validateur
    JOIN personnel per        ON per.id_personnel = m.id_personnel
 
    WHERE r.id_nuit = p_id_nuit;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-22 11:24:02
