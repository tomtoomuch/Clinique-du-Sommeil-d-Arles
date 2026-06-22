const {connex} = require('../db.js');
const db = connex;

function findUserByMailAndPassword(email, password, callback) {
    return new Promise ((resolve,reject) => { 
        db.query('SELECT id, email, password, role FROM personnel WHERE email = ? AND password = ?;',
            [email, password],
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


module.exports = {findUserByMailAndPassword}