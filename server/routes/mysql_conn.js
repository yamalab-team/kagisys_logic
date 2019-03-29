var mysql = require("mysql2");
const Parser = require("configparser");
const config = new Parser();
config.read('/home/pi/project/kagisys_logic/kagisys.conf');
config.sections();
var SQLURL = config.get("MYSQL", "url");
var connection = mysql.createConnection(SQLURL);
module.exports = connection;
