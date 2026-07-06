const { findUserByMailAndPassword } = require('../modelsCrud/loginModel');
const { findUserJob } = require('../modelsCrud/loginModel');
const { getPerso } = require('../modelsCrud/loginModel');
const { getInfoPerso } = require('../modelsCrud/loginModel');
const { ChangeNamePerso } = require('../modelsCrud/loginModel');
const { ChangePrenomPerso } = require('../modelsCrud/loginModel');
const { ChangeEmailPerso } = require('../modelsCrud/loginModel');
const { ChangePhonePerso } = require('../modelsCrud/loginModel');
const { ChangeActifPerso } = require('../modelsCrud/loginModel');

connexionUtilisateur = async (req, res) => {
    const { email, password } = req.body
    const userFound = await findUserByMailAndPassword(email, password);
    if (!userFound) {
        return res.status(404).json({
            success: false,
            message: "Identifiants invalides"
        })
    }
    return res.status(200).json({
        success: true,
        message: "Connexion validée",
        email: userFound.email,
        prenom: userFound.prenom,
        nom:userFound.nom,
        telephone:userFound.telephone,
        id: userFound.id_personnel,
        date_embauche: userFound.date_embauche
    })
}

findJob = async (req, res) => {
    const { id_personnel } = req.query;

    const jobFound = await findUserJob(Number(id_personnel));

    if (!jobFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Personnel trouvé",
        job: jobFound
    });
}

getPersonnel = async (req,res) => {
    const tout = await getPerso();
    return res.status(200).json({
            "personnel" : tout
        })
}

getInfoPersonnel = async (req, res) => {
    const { id_personnel } = req.query;

    const infoPersoFound = await getInfoPerso(Number(id_personnel));

    if (!infoPersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Personnel trouvé",
        infoPerso: infoPersoFound,
        email: infoPersoFound.email,
        prenom: infoPersoFound.prenom,
        nom:infoPersoFound.nom,
        telephone:infoPersoFound.telephone,
        id: infoPersoFound.id_personnel,
        date_embauche: infoPersoFound.date_embauche
    });
}

changeNamePersonnel = async (req, res) => {
    const { id_personnel } = req.body;
    const { nom } = req.body;


    const PersoFound = await ChangeNamePerso(nom, Number(id_personnel));

    if (!PersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Nom changé",
        nom:PersoFound.nom,
        
    });
}

changePrenomPersonnel = async (req, res) => {
    const { id_personnel } = req.body;
    const { prenom } = req.body;


    const PersoFound = await ChangePrenomPerso(prenom, Number(id_personnel));

    if (!PersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Prenom changé",
        prenom:PersoFound.prenom,
        
    });
}

changeEmailPersonnel = async (req, res) => {
    const { id_personnel } = req.body;
    const { email } = req.body;


    const PersoFound = await ChangeEmailPerso(email, Number(id_personnel));

    if (!PersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Email changé",
        email:PersoFound.email,
        
    });
}

changePhonePersonnel = async (req, res) => {
    const { id_personnel } = req.body;
    const { telephone } = req.body;


    const PersoFound = await ChangePhonePerso(telephone, Number(id_personnel));

    if (!PersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Téléphone changé",
        telephone:PersoFound.telephone,
        
    });
}

changeActifPersonnel = async (req, res) => {
    const { id_personnel } = req.body;
    const { actif } = req.body;


    const PersoFound = await ChangeActifPerso(actif, Number(id_personnel));

    if (!PersoFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de personnel..."
        });
    }

    return res.status(200).json({
        success: true,
        message: "Actif changé",
        actif:PersoFound.actif,
        
    });
}


module.exports = { connexionUtilisateur,findJob,getPersonnel,getInfoPersonnel, changeNamePersonnel,changePrenomPersonnel, 
    changeEmailPersonnel, changePhonePersonnel, changeActifPersonnel }; 
