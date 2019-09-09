// app.js
const chef = require("cyberchef");

var text = '';

process.stdin.setEncoding('utf8');
process.stdin.on('readable', function () {
  var chunk = process.stdin.read();
  if (chunk !== null) {
    text += chunk;
  }
});
process.stdin.on('end', function () {
    console.log(chef.fromHex(text));
});



// node app.js
// => "So long and thanks for all the fish."