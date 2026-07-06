const {connexion} = require('../db.js');



function getPatients(){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * FROM patient;', 
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

module.exports = {getPatients}
