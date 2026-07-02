const {connexion} = require('../db.js');


function findUserByMailAndPassword(email, password) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT * FROM personnel WHERE email = ? AND password = ?;',
            [email, password],
            (err,row) => {
                if (err){
                        console.log(err.message);
                        return reject(err, null);
                }
                if (row){
                    resolve(row[0]);
                }
            });
    });
};


function findUserJob(id_personnel) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT "infirmier" AS source FROM infirmier WHERE id_personnel = ? UNION ALL SELECT "medecin" AS source FROM medecin WHERE id_personnel = ? ;',
            [id_personnel,id_personnel],
            (err,row) => {
                if (err){
                        console.log(err.message);
                        return reject(err, null);
                }
                if (row){
                    resolve(row[0]);
                    
                }
            });
    });
};
module.exports = {findUserByMailAndPassword,findUserJob}
