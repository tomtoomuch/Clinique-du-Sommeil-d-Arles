const {connexion} = require('../db.js');


function findUserByMailAndPassword(email, password) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT id_personnel, email, password FROM personnel WHERE email = ? AND password = ?;',
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

module.exports = {findUserByMailAndPassword}