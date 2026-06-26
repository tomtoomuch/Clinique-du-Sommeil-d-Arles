const { findUserByMailAndPassword } = require('../modelsCrud/loginModel');

connexionUtilisateur = async (req, res) => {
    const { email, pass } = req.body
    const userFound = await findUserByMailAndPassword(email, pass);
    if (!userFound) {
        return res.status(404).json({
            success: false,
            message: "Identifiants invalides"
        })
    }
    return res.status(200).json({
        success: true,
        message: "Connexion validée"
    })
}

module.exports = { connexionUtilisateur }; 