const { connexion } = require('../db.js');
const db = connexion;

function findUserByMailAndPassword(email, password) {
    return new Promise((resolve, reject) => {
        db.query('SELECT id_personnel, email, password FROM personnel WHERE email = ? AND password = ?;',
            [email, password],
            (err, row) => {
                if (err) {
                    console.log(err.message);
                    return reject(err, null);
                }
                if (row) {
                    resolve(row[0]);
                }
            });
    });
};


module.exports = { findUserByMailAndPassword }