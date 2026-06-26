const {connexion} = require('../db.js');


function findUserByMailAndPassword(email, pass) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT id_personnel, email, pass FROM personnel WHERE email = ? AND pass = ?;',
            [email, pass],
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