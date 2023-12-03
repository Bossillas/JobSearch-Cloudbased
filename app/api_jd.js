const dbConnection = require('./database.js');
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

const uuid = require('uuid');

exports.post_jd = async (req, res) => {
  console.log("call to /image...");

  try {
    // const jobId = req.params.jobid;
    var data1 = req.body;
    const jobId = data1.jobid
    const data = data1.data;
    console.log(jobId);
    console.log(data);
    console.log("hi");

    // Check if the user exists
    dbConnection.query('SELECT title FROM jobs WHERE id = ?', [jobId], async (err, result) => {
      if (err) throw err;

      if (result.length === 0) {
        return res.status(400).json({
          "message": "no such job...",
          "assetid": -1
        });
      }

      const bucketfolder = "jobdescription";

      // Decode the base64 image
      const bytes = Buffer.from(data, 'base64');

      // Generate a unique name for the asset
      const newJD = uuid.v4();
      const uniqueKey = `${bucketfolder}/${newJD}.txt`;

      // Upload to S3
      const uploadParams = {
        Bucket: s3_bucket_name,
        Key: uniqueKey,
        Body: bytes,
        ContentType: "text/plain"
      };

      await s3.send(new PutObjectCommand(uploadParams));

      // update description in jobs table
      const updateQuery = 'UPDATE jobs SET description = ? WHERE id = ?';
      dbConnection.query(updateQuery, [newJD, jobId], (updateErr, updateResult) => {
        if (updateErr) {
          // Handle the error, possibly by logging it and sending a response to the client
          console.error("Error updating job description in the database:", updateErr);
          res.status(500).send("Error updating job description in the database.");
        } else {
          if (updateResult.affectedRows > 0) {
            console.log("Job description updated successfully in the database.");
            res.json({
              "message": "File uploaded to S3 and job description updated successfully",
              "jobId": jobId,
              "description": newJD
            });
          } else {
            // No rows were updated, which means the job ID was not found
            console.error("No job found with the provided ID.");
            res.status(404).send("Job not found.");
          }
        }
      });
      //const insertQuery = 'INSERT INTO assets (userid, assetname, bucketkey) VALUES (?, ?, ?)';
    //   const updateQuery = 'UPDATE jobs SET description = ? WHERE id = ?';
    //   dbConnection.query(updateQuery, [newJD, jobId], (err, insertResult) => {
    //     if (err) throw err;

    //     res.json({
    //       "message": "success",
    //       "assetid": insertResult.insertId
    //     });
    //   });

    });
  } catch (err) {
    console.log("**ERROR:", err.message);
    res.status(400).json({
      "message": err.message,
      "assetid": -1
    });
  }
}
