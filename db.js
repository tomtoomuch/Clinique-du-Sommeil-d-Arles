const db = require('mysql');

const connex = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : '123456789',
    database: 'resultatsnuitsommeil',
    port: '3306'
})
// modifier les identifiants pour acceder à la BDD



module.exports = {connex}