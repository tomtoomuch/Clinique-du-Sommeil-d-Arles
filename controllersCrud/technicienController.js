const {vueTechniecienCpap} = require('../modelsCrud/technicienModel');

exports.vueCpap = async (req,res) => {
    const tout = await vueTechniecienCpap();
    return res.status(200).json({
            "medecin" : tout
        })
}