const {connex} = require('../db.js');
const db = connex;

function getMedecin(){
    return new Promise ((resolve,reject) => { 
        db.query('SELECT * from medecin;', (err,rows) => {
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