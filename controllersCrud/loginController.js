const {findUserByMailAndPassword} = require('../modelsCrud/loginModel');

connexionUtilisateur = async (req,res) => {
    const { email, password } = req.body
    const userFound = await findUserByMailAndPassword(email,password);
     
    if(!userFound) {
        return res.status(404).json({
            success: false,
            message: "Identifiants invalides"
        })
    }

    return res.status(200).json({
        success: true,
        message: "Connexion validée",
    })
}

module.exports = { connexionUtilisateur };