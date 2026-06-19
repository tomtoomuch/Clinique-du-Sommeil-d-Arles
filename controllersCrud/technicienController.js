const {vueTechniecienCpap, vueTechniecienPsg} = require('../modelsCrud/technicienModel');

exports.vueCpap = async (req,res) => {
    const tout = await vueTechniecienCpap();
    return res.status(200).json({
            "vue cpap" : tout
        })
}

exports.vuePsg = async (req,res) => {
    const tout = await vueTechniecienPsg();
    return res.status(200).json({
            "vue psg" : tout
        })
}