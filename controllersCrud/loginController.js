const {loginUtilisateur} = require('../modelsCrud/loginModel');

exports.connexionUtilisateur = async (req,res) => {
    const login = await findUserByMailAndPassword();
    return res.status(200).json({
            success: true,
            message: "Connexion validée",
            id: user.id,
            role: user.role
        })
}