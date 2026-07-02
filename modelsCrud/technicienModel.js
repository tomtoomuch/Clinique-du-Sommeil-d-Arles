const {connexion} = require('../db.js');


function vueTechniecienCpap(){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * from vuetechnieciencpap;', (err,rows) => {
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


function vueTechniecienPsg(){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * from vuetechnicienpsg;', (err,rows) => {
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

function findNuitDispo() {
    return new Promise ((resolve,reject) => {
        connexion.query("SELECT * FROM nuit_disponible;",
            
            (err,row) => {
                if (err){
                        console.log(err.message);
                        return reject(err, null);
                }
                if (row){
                    resolve(row);
                    
                }
            });
    });
};
module.exports = {vueTechniecienCpap, vueTechniecienPsg, findNuitDispo}
