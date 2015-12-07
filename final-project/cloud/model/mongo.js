var mongoose = require("mongoose");

mongoose.connect('mongodb://localhost:27017/messages');
var mongoSchema = mongoose.Schema;
var userSchema = {
  "message" : {type:String, required:true},
  "location" : {type:[Number], required:true},
  "id": {type:String, required:true}
};

module.exports = mongoose.model('messages',userSchema);
