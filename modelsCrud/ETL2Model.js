const {connexion} = require('../db.js');
const { spawn } = require("child_process");
const express = require("express");
const router = express.Router();


router.get('/lancerETL2', lancerScript);

function lancerScript(req, res) {

    const pythonProcess = spawn('python', [
        "./ETL2.py",
        req.query.id_patient
       
    ]);

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {

        // CAS ERREUR PYTHON
        if (code !== 0) {
            return res.status(500).send({
                success: false,
                message: "Erreur lors de l'exécution du script Python",
                error: errorOutput.trim()
            });
        }

        // CAS PYTHON MAIS AVEC MESSAGE D'ERREUR LOGIQUE
        if (errorOutput) {
            return res.status(400).send({
                success: false,
                message: "Le script Python a retourné une erreur",
                error: errorOutput.trim()
            });
        }

        //  CAS SUCCÈS
        return res.send({
            success: true,
            message: "Script exécuté avec succès",
            data: output.trim()
        });
    });
}

module.exports = router;