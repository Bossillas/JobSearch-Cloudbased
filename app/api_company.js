const dbConnection = require('./database.js');

exports.put_company = async (req, res) => {
    console.log("call to /company...");

    try {
        var data = req.body; // data => JS object
        console.log(data);
        console.log(data.industry);

        // First, get the industry_id from the Industries table using the industry name
        dbConnection.query('SELECT id FROM industries WHERE industry = ?', [data.industry], (industryErr, industryResult) => {
            if (industryErr) throw industryErr;

            if (industryResult.length === 0) {
                // Industry does not exist, handle accordingly
                res.status(404).json({
                    "message": "Industry not found",
                });
            } else {
                // Industry exists, proceed to check if the company name exists
                console.log(industryResult[0]);
                const industryId = industryResult[0].id;
                console.log(industryId);
              

                dbConnection.query('SELECT id FROM companies WHERE name = ?', [data.name], (companyErr, companyResult) => {
                    if (companyErr) throw companyErr;

                    if (companyResult.length > 0) {
                        // Company exists, don't insert
                        res.json({
                            "message": "Company already exists",
                            "companyId": companyResult[0].ID
                        });
                    } else {
                        // Company doesn't exist, so insert
                        const insertQuery = `
                            INSERT INTO companies (name, industry_id, location)
                            VALUES (?, ?, ?)
                        `;
                        dbConnection.query(insertQuery, [data.name, industryId, data.location], (insertErr, insertResult) => {
                            if (insertErr) throw insertErr;

                            if (insertResult.affectedRows == 1) {
                                res.json({
                                    "message": "Company inserted",
                                    "companyId": insertResult.insertId
                                });
                            } else {
                                throw new Error("Failed to insert company.");
                            }
                        });
                    }
                });
            }
        });
    } catch (err) {
        console.log("**ERROR:", err.message);
        res.status(400).json({
            "message": err.message,
            "companyId": -1
        });
    }
};
