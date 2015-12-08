var express = require("express");

var app = express();
var bodyParser = require("body-parser");
var router = express.Router();
var mongoOp = require('./model/mongo')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({'extended' : false}));

router.get('/',function(req,res){
    console.log('GET /');

    res.json({'error': false,'message': 'GET and POST /messages'});
});

router.route('/messages')
    .get(function(req,res){
        console.log('GET /messages');

        var response = {};
        mongoOp.find({location:{$near:{$geometry:{type:"Point",coordinates:[req.query.longitude,req.query.latitude]},}}}).limit(50).exec(function(err,data){
            if (err) {
                console.log(err);
                response = {'error': true,'message': 'Error fetching data. Please specify latitude and longitude.'};
            } else {
                response = {'error': false,'message': data};
            }
            res.json(response);
        });
    })
    .post(function(req,res) {
        console.log('POST /messages');

        var db = new mongoOp();
        var response = {};

        db.message = req.body.message;
        db.location = [req.body.longitude,req.body.latitude];
        db.id = req.body.id;

        db.save(function(err) {
            if(err) {
                console.log(err);
                response = {'error': true,'message': 'Error adding data. Please specify id, message, latitude, and longitude.'};
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
