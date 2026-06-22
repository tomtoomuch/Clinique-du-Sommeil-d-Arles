const {loginUtilisateur} = require('../modelsCrud/loginModel');

exports.connexionUtilisateur = async (req,res) => {
    const { email, password } = req.body
    const login = await findUserByMailAndPassword(email,password);
    return res.status(200).json({
            success: true,
            message: "Connexion validée",
            id: user.id,
            role: user.role
        })
}