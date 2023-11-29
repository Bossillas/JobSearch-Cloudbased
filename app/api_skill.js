const dbConnection = require('./database.js')

exports.put_skill = async (req, res) => {
    console.log("call to /skill...");

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
        
        var sql = "SELECT id FROM skills WHERE skill = ?";
        var rds_response = await queryAsync(sql, [data.skill]);

        if (rds_response.length > 0) {
            // skill already exist, just return no change
            return res.status(200).json({
                "message": "Skill already exists",
                "skillId": rds_response[0].ID
            });
        } else {
            // skill doesn't exist, need to add new skill
            var sql = `INSERT INTO skills (skill) VALUES (?)`;
            var rds_response = queryAsync(sql, [data.skill]);
            rds_response.then(result => {
                return res.status(200).json({
                    "message": "Skill inserted",
                    "skillId": result.insertId
                });
            }).catch(err => {
                return res.status(400).json({
                    "message": err.message,
                    "skillId": -1
                });
            })
        }
    }
    catch (err) {
        res.status(400).json({
            "message": err.message,
            "skillId": -1
        });
    }
}