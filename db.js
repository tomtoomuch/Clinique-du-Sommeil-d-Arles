const db = require('mysql2');
const {motDePasse, bdd, port} = require('./mdp.js')

const connexion = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : motDePasse,
    database: bdd,
    port: port
})

connexion.connect((err) => {
  if (err) {
    console.error("Erreur connexion MySQL :", err.message);
    return;
  }
  console.log("Connexion MySQL OK");
});

module.exports = {connexion}