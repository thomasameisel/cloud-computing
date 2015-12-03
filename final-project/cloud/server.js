var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var router = express.Router();
var mongoOp = require('./model/mongo')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({'extended' : false}));

router.get('/',function(req,res){
    res.json({"error" : false,"message" : 'Hello World'});
});

router.route('/messages')
    .get(function(req,res){
        var response = {};
        mongoOp.find({},function(err,data){
            if (err) {
                response = {'error': true,'message': 'Error fetching data'};
            } else {
                response = {'error': false,'message': data};
            }
            res.json(response);
        });
    })
    .post(function(req,res) {
        var db = new mongoOp();
        var response = {};

        db.message = req.body.message;
        db.location = req.body.location;
        db.id = req.body.id;

        db.save(function(err) {
            if(err) {
                response = {'error': true,'message': 'Error adding data'};
            } else {
                response = {'error': false,'message': 'Data added'};
            }
            res.json(response);
        });
    });

app.use('/',router);

var port = 3000;
app.listen(port);
console.log('Listening to port', port);