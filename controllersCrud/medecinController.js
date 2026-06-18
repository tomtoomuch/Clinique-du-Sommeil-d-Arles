const {getMedecin} = require('../modelsCrud/medecinModel');

exports.afficherTout = async (req,res) => {
    const tout = await getAllUser();
    return res.status(200).json({
            "medecin" : tout
        })
}