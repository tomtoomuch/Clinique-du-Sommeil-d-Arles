const express = require("express");
const loginController = require('../controllersCrud/loginController');
const router = express.Router();

router.post('/login', loginController.connexionUtilisateur);

module.exports = router;