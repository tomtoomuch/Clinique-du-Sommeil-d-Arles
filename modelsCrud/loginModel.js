const {connex} = require('../db.js');
const db = connex;

function findUserByMailAndPassword(mail, password, callback) {
    return new Promise ((resolve,reject) => { 
        db.query('SELECT id, mail, password, role FROM users WHERE mail = ? AND password = ?;',
            [mail, password],
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