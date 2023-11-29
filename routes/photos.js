const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });


router.post('/getimg', upload.single('photo'), (req, res) => {
  console.log(req.file);

  // Run the Python script
  const python = spawn('python', ['./routes//predict.py']);

  // Collect data from the script
  let scriptOutput = '';
  python.stdout.on('data', (data) => {
      scriptOutput += data.toString();
      console.log(scriptOutput);
  });
  python.stderr.on('data', (data) => {
    console.error(`Python script stderr: ${data}`);
});
  python.on('error', (error) => {
  console.error(`child process encountered an error ${error}`);
});

  // Handle script completion
  python.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`);
      
      // Send the script output as the response
      res.send(scriptOutput);
  });

  python.on('error', (error) => {
      console.log(`child process encountered an error ${error}`);
      res.status(500).send(error);
  });
  
}); 




router.post('/getimg',(req,res)=>{
    console.log(req.body);
    res.sendStatus(200);

})

module.exports = router;