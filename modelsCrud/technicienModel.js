const {connex} = require('../db.js');
const db = connex;

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



module.exports = {vueTechniecienCpap}