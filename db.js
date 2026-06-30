const db = require('mysql2');
const {motDePasse, bdd, port} = require('./mdp.js')
<<<<<<< HEAD
=======
console.log(motDePasse)
>>>>>>> dev
const connexion = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : motDePasse,
    database: bdd,
    port: port
})
<<<<<<< HEAD

connexion.connect((err) => {
  if (err) {
    console.error("Erreur connexion MySQL :", err.message);
    return;
  }
  console.log("Connexion MySQL OK");
});
=======
>>>>>>> dev

connexion.connect((err) => {
  if (err) {
    console.error("Erreur connexion MySQL :", err.message);
    return;
  }
  console.log("Connexion MySQL OK");
});

module.exports = {connexion}