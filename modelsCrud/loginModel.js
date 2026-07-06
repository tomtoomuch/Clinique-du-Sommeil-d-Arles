const {connexion} = require('../db.js');


function findUserByMailAndPassword(email, password) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT * FROM personnel WHERE email = ? AND password = ?;',
            [email, password],
            (err, row) => {
                if (err) {
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
    return new Promise((resolve, reject) => {
        connexion.query(
            'SELECT "infirmier" AS source FROM infirmier WHERE id_personnel = ? \
             UNION ALL \
             SELECT "medecin" AS source FROM medecin WHERE id_personnel = ? \
             UNION ALL \
             SELECT "rh" AS source FROM rh WHERE id_personnel = ?;',
            [id_personnel, id_personnel, id_personnel],
            (err, row) => {
                if (err) {
                    console.log(err.message);
                    return reject(err);
                }
                if (row) {
                    resolve(row[0]);
                } else {
                    resolve(null);
                }
            }
        );
    });
}
function getPerso(){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * FROM personnel;', 
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

function getInfoPerso(id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('SELECT * FROM personnel WHERE id_personnel = ?;', 
            [id_personnel],
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

function ChangeNamePerso(nom, id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('UPDATE personnel set nom = ? WHERE id_personnel = ?;', 
            [nom, id_personnel],
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

function ChangePrenomPerso(prenom, id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('UPDATE personnel set prenom = ? WHERE id_personnel = ?;', 
            [prenom, id_personnel],
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

function ChangeEmailPerso(email, id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('UPDATE personnel set email = ? WHERE id_personnel = ?;', 
            [email, id_personnel],
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

function ChangePhonePerso(telephone, id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('UPDATE personnel set telephone = ? WHERE id_personnel = ?;', 
            [telephone, id_personnel],
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

function ChangeActifPerso(actif, id_personnel){
    return new Promise ((resolve,reject) => { 
        connexion.query('UPDATE personnel set actif = ? WHERE id_personnel = ?;', 
            [actif, id_personnel],
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

module.exports = {findUserByMailAndPassword,findUserJob,getPerso,getInfoPerso, ChangeNamePerso, ChangePrenomPerso,
     ChangeEmailPerso, ChangePhonePerso, ChangeActifPerso}
