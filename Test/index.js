var Client = require('node-rest-client').Client;
var fs = require('fs');
var readline = require('readline');
var client = new Client();
var dataQueue=[];

var rd = readline.createInterface({
  input: fs.createReadStream('sample2.txt')
})

rd.on('line', function(line) {
  dataQueue.push(line);
})

function postData(){
  if(dataQueue.length == 0)
    return;
  var fileData = dataQueue.shift();
  var args = {
      data: { value: fileData, timeStamp: new Date() },
      headers: { "Content-Type": "application/json" }
  };
  console.log(`Sending ${fileData} to API`)
  client.post("http://127.0.0.1:5000/postJson", args, function (data, response) {
      console.log(data.toString('utf8'));
  });
}

setInterval(postData, 3000);
