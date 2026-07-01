const {vueTechniecienCpap, vueTechniecienPsg} = require('../modelsCrud/technicienModel');
const {findNuitDispo} = require('../modelsCrud/technicienModel');

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

exports.nuitDispo = async (req, res) => {
    
    const nuitFound = await findNuitDispo();

    if (!nuitFound) {
        return res.status(404).json({
            success: false,
            message: "Pas de nuit dispo..."
        });
    }
    console.log(res)
    return res.status(200).json({
        success: true,
        message: "Nuit trouvée",
        nuitsTrouvees : nuitFound
        
    });
}
