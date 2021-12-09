const express = require('express')
const {spawn} = require('child_process');
const app = express()
const port = 3000


app.use(express.static("public"))
app.use(express.urlencoded({ extended: true} ))

var python;


// app.get('/', (req, res) => {
 
//  var dataToSend;
//  // spawn new child process to call the python script
//  run('sample.py')
//  // collect data from script
//  python.stdout.on('data', function (data) {
//   console.log('Pipe data from python script ...');
//   dataToSend = data.toString();
//  });
//  // in close event we are sure that stream from child process is closed
//  python.on('close', (code) => {
//  console.log(`child process close all stdio with code ${code}`);
//  // send data to browser
//  res.send(dataToSend)
//  });
 
// })

app.post("/", (req, res) => {
    var dataToSend;
    run(req.body.fileName, function() {
        // collect data from script
        python.stdout.on('data', function (data) {
            console.log('Pipe data from python script ...');
            dataToSend = data.toString();
        });
        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
        });
    })
})

app.listen(port, () => console.log(`Example app listening on port http://localhost:3000/`))


function run(fn, callback){
    python = spawn('python', [fn]);
    callback();
}