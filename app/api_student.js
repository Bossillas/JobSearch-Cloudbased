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

        function createPlaceholders(list) {
            return list.map(() => '?').join(',');
        }
        function values_skill_major(student_id, len) {
            let result = '';
            for (let i = 0; i < len; i++) {
                result += `(${student_id}, ?)`;
                if (i < len - 1) {
                    result += ', ';
                }
            }
            return result;
        }
        
        var sql_school = "SELECT id FROM schools WHERE name = ?";
        var sql_skill = "SELECT id FROM skills WHERE skill IN (" + createPlaceholders(data.skill) + ")";
        var sql_major = "SELECT id FROM majors WHERE major IN (" + createPlaceholders(data.major) + ")";
        var rds_school = queryAsync(sql_school, [data.school]);
        var rds_skill = queryAsync(sql_skill, data.skill);
        var rds_major = queryAsync(sql_major, data.major);

        Promise.all([rds_school, rds_skill, rds_major]).then(async results => {
            if (results[0].length === 0 || results[1].length < data.skill.length || results[2].length < data.major.length) {
                return res.status(400).json({
                    "message": "Foreign Key Error when updating students table",
                    "studentId": -1
                });
            }
            var sql = `INSERT INTO students (firstname, lastname, email, linkedin, resume_s3, school_id)
                        VALUES (?, ?, ?, ?, ?, ?);`;
            var rds_response = await queryAsync(sql, [data.firstname, data.lastname, data.email, data.linkedin, data.resume_s3, results[0][0]["id"]]);

            var student_id = rds_response.insertId;

            var sql_student_skill = `INSERT INTO student_skill (student_id, skill_id)
                                    VALUES` + values_skill_major(student_id, data.skill.length) + `;`;
            var sql_student_major = `INSERT INTO student_major (student_id, major_id)
                                    VALUES` + values_skill_major(student_id, data.major.length) + `;`;
            var rds_skill_res = queryAsync(sql_student_skill, results[1]["id"]);
            var rds_major_res = queryAsync(sql_student_major, results[2]["id"]);

            Promise.all([rds_skill_res, rds_major_res]).then(results => {
                return res.status(200).json({
                    "message": "Inserted student successfully",
                    "studentId": student_id
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