var express = require('express');
var router = express.Router();
var conn = require("./mysql_conn");
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index');
});

router.post('/add', function(req, res ,next) {
  var idm=req.body.idm;
  var user_name=req.body.user_name;
  var q = 'INSERT INTO nfctag VALUES ("'+ idm + '", "' + user_name + '")';
  conn.query(q, function(err, rows) {
    if(err) {
      console.log(err);
      res.render('comp', {"message": err});
    } else {
      console.log(rows);
      res.render('comp', {"message": "登録完了"});
    }
  });
});

module.exports = router;
