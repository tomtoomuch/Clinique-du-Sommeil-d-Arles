const express = require("express");
const techniciensController = require('../controllersCrud/technicienController');
const router = express.Router();

router.get('/vueCpap', techniciensController.vueCpap);
router.get('/vuePsg', techniciensController.vuePsg);
router.get('/nuitDispo', techniciensController.nuitDispo);

module.exports = router;