var Client = require('node-rest-client').Client;
var fs = require('fs');
var client = new Client();

function postData(){
  var fileData = "";
  fs.readFile('sample2.txt', (err,data)=>{
    if(err) throw err;
    fileData = String.fromCharCode.apply(null, data);
    var args = {
      data: { value: fileData, timeStamp: new Date() },
      headers: { "Content-Type": "application/json" }
    };
    client.post("http://127.0.0.1:5000/postJson", args, function (data, response) {
      console.log(String.fromCharCode.apply(null, data));
    });
  });
}

function getData(){
  var args = {
    headers: { "Content-Type": "application/json" }
  };
  client.get("http://127.0.0.1:5000/getJSON", args, function (data, response) {
    console.log(JSON.parse(data.toString('utf8')));
  });
}
postData()
setTimeout(getData, 3000)