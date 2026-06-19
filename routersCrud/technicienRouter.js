const express = require("express");
const techniciensController = require('../controllersCrud/technicienController');
const router = express.Router();

router.get('/vueCpap', techniciensController.vueCpap);


module.exports = router;