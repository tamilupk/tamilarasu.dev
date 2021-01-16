var express = require('express');
var router = express.Router();
var fs =  require('fs').promises;
var path =  require('path')

/* GET home page. */
router.get('/', async function(req, res, next) {
  var indexPage = await fs.readFile(path.resolve(__dirname, '../views/index.html'));
  res.setHeader('content-type', 'text/html');
  res.send(indexPage)
});

module.exports = router;
