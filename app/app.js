
const express = require('express');
const app = express();
const config = require('./config.js');

const dbConnection = require('./database.js')
const { HeadBucketCommand, ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

app.use(express.json({ strict: false, limit: "50mb" }));

var startTime;

app.listen(config.service_port, () => {
  startTime = Date.now();
  console.log('web service running...');
  //
  // Configure AWS to use our config file:
  //
  process.env.AWS_SHARED_CREDENTIALS_FILE = config.photoapp_config;
});

app.get('/', (req, res) => {

  var uptime = Math.round((Date.now() - startTime) / 1000);

  res.json({
    "status": "running",
    "uptime-in-secs": uptime,
    "dbConnection": dbConnection.state
  });
});

//
// service functions:
//
var stats = require('./api_stats.js');
var users = require('./api_users.js');
var assets = require('./api_assets.js');
// var bucket = require('./api_bucket.js');
// var download = require('./api_download.js');

var industry = require('./api_industry.js');
var company = require('./api_company.js');
var job = require('./api_job.js');

var status = require('./api_status.js');

var major = require('./api_major.js');

var skill = require('./api_skill.js');

var school = require('./api_school.js');

var student = require('./api_student.js');

var resume = require('./api_resume.js');
// var summary = require('./api_job_summary.js');

// var image = require('./api_image.js');

app.get('/stats', stats.get_stats);  //app.get('/stats', (req, res) => {...});
app.get('/users', users.get_users);  //app.get('/users', (req, res) => {...});
app.get('/assets', assets.get_assets);  //app.get('/assets', (req, res) => {...});
// app.get('/bucket', bucket.get_bucket);  //app.get('/bucket?startafter=bucketkey', (req, res) => {...});
// app.get('/download/:assetid', download.get_download); //app.get('/download/:assetid', (req, res) => {...});

app.put('/industry', industry.put_industry); // app.put('/user',(req,res => {...}));

app.put('/company', company.put_company);

app.post('/job', job.post_job);

app.post('/status', status.post_status);

app.put('/major', major.put_major);

app.put('/skill', skill.put_skill);

app.put('/school', school.put_school);

app.put('/student', student.put_student);

app.post('/resume/:id', resume.post_resume);

// app.get('/summary', summary.get_summary);
// app.post('/image/:userid', image.post_image);