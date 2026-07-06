const express = require("express");
const patientController = require('../controllersCrud/patientController');
const router = express.Router();


router.get('/getPatient', patientController.getPatient);


module.exports = router;