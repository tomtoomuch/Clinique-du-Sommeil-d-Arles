const express = require("express"); 
const app = express();
app.use(express.json());

// const loginRoute = require('./routersCrud/loginRouter');


// const medecinRoute = require('./routersCrud/medecinRouter');
// const technicienRoute = require('./routersCrud/technicienRouter');

// app.use("/api/users/", loginRoute);


// app.use("/api/medecin/", medecinRoute);
// app.use("/api/techicien/", technicienRoute);

 const db = require('mysql2');
const {motDePasse, bdd, port} = require('./mdp.js')



const connex = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : motDePasse,
    database: bdd,
    port: port
})


connex.connect((err) => {
  if (err) {
    console.error("Erreur connexion MySQL :", err.message);
    return;
  }
  console.log("Connexion MySQL OK");
});


async function findUserByMailAndPassword(email, password, callback) {

    console.log(1)
    return new Promise ((resolve,reject) => { 
        console.log(2)
        connex.query('SELECT id_personnel, email, password FROM personnel WHERE email = ? AND password = ?;',
            [email, password],
            (err,row) => {
                console.log(3)
                if (err){
                    console.log(4)
                        console.log(err.message);
                        return reject(err, null);
                }
                if (row){
                    console.log(5)
                    console.log(row)
                    resolve(row);
                }
            });
    });
};   

connexionUtilisateur = async (req,res) => {
    const { email, password } = req.body
    const login = await findUserByMailAndPassword(email,password);
    return res.status(200).json({
            success: true,
            message: "Connexion validée"
        })
}

app.post('/login', connexionUtilisateur);

app.listen(3000, () => {
    console.log("Serveur démarré sur le port 3000");
});