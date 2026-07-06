const { getPatients } = require('../modelsCrud/patientModel');




getPatient = async (req,res) => {
    const tout = await getPatients();
    return res.status(200).json({
            "patient" : tout
        })
}


module.exports = { getPatient }; 
