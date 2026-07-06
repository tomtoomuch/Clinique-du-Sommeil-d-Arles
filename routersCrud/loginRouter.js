const express = require("express");
const loginController = require('../controllersCrud/loginController');
const router = express.Router();

router.post('/login', loginController.connexionUtilisateur);
router.get('/job', loginController.findJob);
router.get('/getPersonnel', loginController.getPersonnel);
router.get('/getInfoPersonnel', loginController.getInfoPersonnel);
router.post('/changeNamePersonnel', loginController.changeNamePersonnel);
router.post('/changePrenomPersonnel', loginController.changePrenomPersonnel);
router.post('/changeEmailPersonnel', loginController.changeEmailPersonnel);
router.post('/changePhonePersonnel', loginController.changePhonePersonnel);
router.post('/changeActifPersonnel', loginController.changeActifPersonnel);

module.exports = router;