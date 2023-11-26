const dbConnection = require('./database.js');

exports.put_industry = async (req, res) => {
  console.log("call to /industry...");

  try {
    var data = req.body; // data => JS object
    console.log(data);

    // Check if the industry exists
    dbConnection.query('SELECT id FROM industries WHERE industry = ?', [data.industry], (err, result) => {
      if (err) throw err;

      if (result.length > 0) {
        // Industry exists, don't insert
        res.json({
          "message": "Industry already exists",
          "industryId": result[0].ID
        });
      } else {
        // Industry doesn't exist, so insert
        const insertQuery = `
                    INSERT INTO industries (industry)
                    VALUES (?)
                `;
        dbConnection.query(insertQuery, [data.industry], (err, insertResult) => {
          if (err) throw err;

          if (insertResult.affectedRows == 1) {
            res.json({
              "message": "Industry inserted",
              "industryId": insertResult.insertId
            });
          } else {
            throw new Error("Failed to insert industry.");
          }
        });
      }
    });
  } catch (err) {
    console.log("**ERROR:", err.message);
    res.status(400).json({
      "message": err.message,
      "industryId": -1
    });
  }
};
