const dbConnection = require('./database.js');
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

const uuid = require('uuid');

exports.post_resume = async (req, res) => {
    console.log("call to /resume...");
    try {
        var data = req.body;

        function queryAsync(sql, params) {
            return new Promise((resolve, reject) => {
              dbConnection.query(sql, params, (err, results) => {
                if (err) reject(err);
                else resolve(results);
              });
            });
          }
        
        // check if usedid exist
        var student_id = req.params.id;
        console.log("/resume check if user exist")
        let sql = "SELECT * FROM students WHERE id = ?;";
        const student = await queryAsync(sql, student_id);

        if (student.length === 0) {
            return res.status(400).json({
                "message": "no such student...",
                "s3_key": -1,
                "student_id": -1
            });
        } else {
            // convert base64 data into bytes for s3
            var S = data.data;
            var bytes = Buffer.from(S, "base64");

            // Asset name with .pdf extension
            var name = uuid.v4() + ".pdf";
            var s3_key = "resume/" + name;

            // Upload to s3
            var input = {
                Bucket: s3_bucket_name,
                Key: s3_key,
                Body: bytes
            }
            console.log("/resume uploading to s3")
            var s3_put_object_command = new PutObjectCommand(input);
            var s3_response = s3.send(s3_put_object_command);

            // insert into database
            console.log("/resume updating database");
            sql = `UPDATE students SET resume_s3 = ?
                    WHERE id = ?;`;
            var rds_response = queryAsync(sql, [name, student_id]);

            // handle promises
            console.log("/resume sending response...");
            Promise.all([s3_response, rds_response]).then(results => {
                res.status(200).json({
                    "message": "success",
                    "s3_key": name,
                    "student_id": student_id
                });
            }).catch(err => {
                res.status(400).json({
                    "message": err.message,
                    "s3_key": -1,
                    "student_id": -1
                });
            })

        }
    } catch (err) {
        res.status(400).json({
            "message": err.message,
            "s3_key": -1,
            "student_id": -1
        });
    }
}