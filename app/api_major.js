const dbConnection = require('./database.js')

exports.put_major = async (req, res) => {
    console.log("call to /major...");

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
        
        var sql = "SELECT id FROM majors WHERE major = ?";
        var rds_response = await queryAsync(sql, [data.major]);

        if (rds_response.length > 0) {
            // major already exist, just return no change
            return res.status(200).json({
                "message": "Major already exists",
                "majorId": rds_response[0].ID
            });
        } else {
            // major doesn't exist, need to add new major
            var sql = `INSERT INTO majors (major) VALUES (?)`;
            var rds_response = queryAsync(sql, [data.major]);
            rds_response.then(result => {
                return res.status(200).json({
                    "message": "Major inserted",
                    "majorId": result.insertId
                });
            }).catch(err => {
                return res.status(400).json({
                    "message": err.message,
                    "majorId": -1
                });
            })
        }
    }
    catch (err) {
        res.status(400).json({
            "message": err.message,
            "majorId": -1
        });
    }
}