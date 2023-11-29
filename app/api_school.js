const dbConnection = require('./database.js')

exports.put_school = async (req, res) => {
    console.log("call to /school...");

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
        
        var sql = "SELECT id FROM schools WHERE name = ?";
        var rds_response = await queryAsync(sql, [data.school]);

        if (rds_response.length > 0) {
            // school already exist, just return no change
            return res.status(200).json({
                "message": "School already exists",
                "schoolId": rds_response[0].ID
            });
        } else {
            // school doesn't exist, need to add new school
            var sql = `INSERT INTO schools (name) VALUES (?)`;
            var rds_response = queryAsync(sql, [data.school]);
            rds_response.then(result => {
                return res.status(200).json({
                    "message": "School inserted",
                    "schoolId": result.insertId
                });
            }).catch(err => {
                return res.status(400).json({
                    "message": err.message,
                    "schoolId": -1
                });
            })
        }
    }
    catch (err) {
        res.status(400).json({
            "message": err.message,
            "schoolId": -1
        });
    }
}