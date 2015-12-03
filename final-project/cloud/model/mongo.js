var mongoose = require("mongoose");

mongoose.connect('mongodb://localhost:27017/demoDb');
var mongoSchema = mongoose.Schema;
var userSchema = {
    "message" : String,
    "location" : String,
    "id": String
};

module.exports = mongoose.model('messages',userSchema);