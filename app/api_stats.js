// app.get('/stats', async (req, res) => {...});
//
// return some stats about our bucket and database:
//
const dbConnection = require('./database.js')
const { HeadBucketCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_stats = async (req, res) => {

  console.log("call to /stats...");

  try {
    var input = {
      Bucket: s3_bucket_name
    };

    console.log("/stats: calling S3...");

    var command = new HeadBucketCommand(input);
    var s3_response = s3.send(command);

    var rds_response = new Promise((resolve, reject) => {
      try {
        console.log("/stats: calling RDS...");

        var sql = `
          Select count(*) As NumStudents From students;
          Select count(*) As NumJobs From jobs;
          Select count(*) As NumCompanies From companies; 
        `;

        dbConnection.query(sql, (err, results, _) => {
          try {
            if (err) {
              console.log("fail sql.");
              reject(err);
              return;
            }

            console.log("/stats query done");
            resolve(results);
          }
          catch (code_err) {
            reject(code_err);
          }
        });
      }
      catch (code_err) {
        reject(code_err);
      }
    });

    Promise.all([s3_response, rds_response]).then(results => {
      try {
        var s3_result = results[0];
        var rds_results = results[1];

        var metadata = s3_result["$metadata"];

        var rows_r1 = rds_results[0];
        var rows_r2 = rds_results[1];
        var rows_r3 = rds_results[2];  // Handle the new result set

        var row_r1 = rows_r1[0];
        var row_r2 = rows_r2[0];
        var row_r3 = rows_r3[0];  // Get the first row from the new result set

        console.log("/stats done, sending response...");

        res.json({
          "message": "success",
          "s3_status": metadata["httpStatusCode"],
          "db_numStudents": row_r1["NumStudents"],
          "db_NumJobs": row_r2["NumJobs"],
          "db_NumCompanies": row_r3["NumCompanies"]  // Add this line
        });
      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "s3_status": -1,
          "db_numStudents": -1,
          "db_NumJobs": -1,
          "db_NumCompanies": -1  // Add this line
        });
      }
    }).catch(err => {
      res.status(400).json({
        "message": err.message,
        "s3_status": -1,
        "db_numStudents": -1,
        "db_NumJobs": -1,
        "db_NumCompanies": -1  // Add this line
      });
    });

  }
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "s3_status": -1,
      "db_numStudents": -1,
      "db_NumJobs": -1,
      "db_NumCompanies": -1  // Add this line
    });
  }

}
