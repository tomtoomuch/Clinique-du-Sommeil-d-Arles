const {connexion} = require('../db.js');
const db = connexion;

function vueTechniecienCpap(){
    return new Promise ((resolve,reject) => { 
        db.query('SELECT * from vuetechnieciencpap;', (err,rows) => {
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
        db.query('SELECT * from vuetechnicienpsg;', (err,rows) => {
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


module.exports = {vueTechniecienCpap, vueTechniecienPsg}