<<<<<<< HEAD
const {findUserByMailAndPassword} = require('../modelsCrud/loginModel');

connexionUtilisateur = async (req,res) => {
    const { email, password } = req.body
    const userFound = await findUserByMailAndPassword(email,password);
     
    if(!userFound) {
=======
const { findUserByMailAndPassword } = require('../modelsCrud/loginModel');

connexionUtilisateur = async (req, res) => {
    const { email, password } = req.body
    const userFound = await findUserByMailAndPassword(email, password);
    if (!userFound) {
>>>>>>> dev
        return res.status(404).json({
            success: false,
            message: "Identifiants invalides"
        })
    }
<<<<<<< HEAD

    return res.status(200).json({
        success: true,
        message: "Connexion validée",
    })
}

module.exports = { connexionUtilisateur };
=======
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

module.exports = { connexionUtilisateur }; 
>>>>>>> dev
