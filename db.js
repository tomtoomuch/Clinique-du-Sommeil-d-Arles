const db = require('mysql');

const connex = db.createConnection({
    host : 'localhost',
    user : 'root',
    password : '123456789',
    database: 'resultatsnuitsommeil',
    port: '3306'
})




module.exports = {connex}