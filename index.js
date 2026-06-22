const express = require("express"); 
const app = express();
app.use(express.json());

const loginRoute = require('./routersCrud/loginRouter');
const medecinRoute = require('./routersCrud/medecinRouter');
const technicienRoute = require('./routersCrud/technicienRouter');
 
app.use("/login", loginRoute);
app.use("/api/medecin/", medecinRoute);
app.use("/api/techicien/", technicienRoute);


app.listen(3000, () => {
    console.log("Serveur démarré sur le port 3000");
});