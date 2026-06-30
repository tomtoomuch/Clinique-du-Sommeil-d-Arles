<<<<<<< HEAD
const { connexion } = require('../db.js');
const db = connexion;

function findUserByMailAndPassword(email, password) {
    return new Promise((resolve, reject) => {
        db.query('SELECT id_personnel, email, password FROM personnel WHERE email = ? AND password = ?;',
=======
const {connexion} = require('../db.js');


function findUserByMailAndPassword(email, password) {
    return new Promise ((resolve,reject) => {
        connexion.query('SELECT * FROM personnel WHERE email = ? AND password = ?;',
>>>>>>> dev
            [email, password],
            (err, row) => {
                if (err) {
                    console.log(err.message);
                    return reject(err, null);
                }
<<<<<<< HEAD
                if (row) {
=======
                if (row){
>>>>>>> dev
                    resolve(row[0]);
                }
            });
    });
};
<<<<<<< HEAD

=======
>>>>>>> dev

module.exports = { findUserByMailAndPassword }