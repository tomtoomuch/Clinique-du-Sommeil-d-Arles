const {connexion} = require('../db.js');
const db = connexion;

function getMedecin(){
    return new Promise ((resolve,reject) => { 
        db.query('SELECT medecin.id_personnel, medecin.specialite, personnel.nom, personnel.prenom FROM medecin LEFT JOIN personnel ON medecin.id_personnel = personnel.id_personnel;', (err,rows) => {
                if (err){
                        console.log(err.message);
                        return reject(err);
                }
                if (rows){
                    resolve(rows);
                }
            })
    })
}


module.exports = {getMedecin}