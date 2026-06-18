const express = require("express");
const medecinsController = require('../controllersCrud/medecinController');
const router = express.Router();

router.get('/tout', medecinsController.afficherTout);

module.exports = router;