const db = require('mysql');
const {motDePasse, bdd, port} = require('./mdp.js')
const connex = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : motDePasse,
    database: bdd,
    port: port
})
// modifier les identifiants pour acceder à la BDD



module.exports = {connex}