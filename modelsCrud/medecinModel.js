const {connexion} = require('../db.js');


function getMedecin(){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * FROM medecin LEFT JOIN personnel ON medecin.id_personnel = personnel.id_personnel;', 
            (err,rows) => {
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