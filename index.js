const express = require("express"); 
const app = express();
app.use(express.json());
const cors = require ('cors');
app.use (cors({
    origin : "http://localhost:4200"
}))

const loginRoute = require('./routersCrud/loginRouter');
const patientRoute = require('./routersCrud/patientRouter');
const medecinRoute = require('./routersCrud/medecinRouter');
const technicienRoute = require('./routersCrud/technicienRouter');
const lancerETL1 = require('./modelsCrud/ETL1Model');
const lancerETL2 = require('./modelsCrud/ETL2Model');

app.use(lancerETL1)
app.use(lancerETL2)
app.use("/api/users/", loginRoute);
app.use("/api/medecin/", medecinRoute);
app.use("/api/technicien/", technicienRoute);
app.use("/api/patient/", patientRoute);



   



// app.post('/login', loginRouteconnexionUtilisateur);

app.listen(3000, () => {
    console.log("Serveur démarré sur le port 3000");
});