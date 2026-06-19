const {connexion} = require('../db.js');
const db = connexion;

function getMedecin(){
    return new Promise ((resolve,reject) => { 
        db.all('SELECT * from medecin;', (err,rows) => {
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