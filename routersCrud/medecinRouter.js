const express = require("express");
const medecinsController = require('../controllersCrud/medecinController');
const router = express.Router();

router.get('/getMedecin', medecinsController.afficherTout);

module.exports = router;