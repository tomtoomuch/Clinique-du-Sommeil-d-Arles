const express = require("express");
const router = express.Router();
const app = express();
app.use(express.json());

const medecinRoute = require('./routersCrud/medecinRouter')
 

app.use(medecinRoute);


app.listen(3000, () => {
    console.log("Serveur démarré sur le port 3000");
});
