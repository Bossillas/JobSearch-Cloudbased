const dbConnection = require('./database.js');

exports.put_student = async (req, res) => {
    console.log("call to /student...");

    try {
        var data = req.body;

        function queryAsync(sql, params) {
            return new Promise((resolve, reject) => {
              dbConnection.query(sql, params, (err, results) => {
                if (err) reject(err);
                else resolve(results);
              });
            });
          };
        
        var sql_school = "SELECT id FROM schools WHERE name = ?";
        var sql_skill = "SELECT id FROM skills WHERE skill = ?";
        var sql_major = "SELECT id FROM majors WHERE major = ?";
        var rds_school = queryAsync(sql_school, [data.school]);
        var rds_skill = queryAsync(sql_skill, [data.skill]);
        var rds_major = queryAsync(sql_major, [data.major]);

        Promise.all([rds_school, rds_skill, rds_major]).then(async results => {
            if (results[0].length === 0 || results[1].length === 0 || results[2].length === 0) {
                return res.status(400).json({
                    "message": "Foreign Key Error when updating students table",
                    "studentId": -1
                });
            }
            var sql = `INSERT INTO students (firstname, lastname, email, linkedin, resume_s3, school_id)
                        VALUES (?, ?, ?, ?, ?, ?);`;
            var rds_response = await queryAsync(sql, [data.firstname, data.lastname, data.email, data.linkedin, data.resume_s3, results[0][0]]);

            rds_response.then(result => {
                return res.status(200).json({
                    "message": "Inserted student successfully",
                    "studentId": result.insertId
                });
            }).catch(err => {
                return res.status(400).json({
                    "message": err.message,
                    "studentId": -1
                });
            })
        }).catch(err => {
            return res.status(400).json({
                "message": err.message,
                "studentId": -1
            });
        });

    }
    catch (err) {
        res.status(400).json({
            "message": err.message,
            "studentId": -1
        });
    }
}