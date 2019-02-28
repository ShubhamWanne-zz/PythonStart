var Client = require('node-rest-client').Client;

var client = new Client();

// set content-type header and data as json in args parameter
var args = {
    data: { test: "hello" },
    headers: { "Content-Type": "application/json" }
};

function postData(){
  client.post("http://127.0.0.1:5000/postJson", args, function (data, response) {
      console.log(data.toString('utf8'));
  });
}
setInterval(postData, 1000)
