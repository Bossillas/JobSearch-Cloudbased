const dbConnection = require('./database.js');

exports.post_job = async (req, res) => {
    console.log("call to /job...");

    try {
        var data = req.body; // data => JS object
        console.log(data);

        // First, check if the job URL already exists
        dbConnection.query('SELECT id FROM jobs WHERE url = ?', [data.url], (urlErr, urlResults) => {
            if (urlErr) {
                return res.status(500).json({
                    "message": urlErr.sqlMessage || "Error querying the job URL.",
                    "error": urlErr
                });
            }

            if (urlResults.length > 0) {
                // Job with URL already exists, don't insert
                return res.status(409).json({
                    "message": "Job with the given URL already exists",
                    "jobId": urlResults[0].id
                });
            }

            // URL does not exist, proceed to check the company name
            dbConnection.query('SELECT id FROM companies WHERE name = ?', [data.company_name], (companyErr, companyResults) => {
                if (companyErr) {
                    return res.status(500).json({
                        "message": companyErr.sqlMessage || "Error querying the company ID.",
                        "error": companyErr
                    });
                }

                if (companyResults.length === 0) {
                    // No matching company found, cannot insert job
                    return res.status(404).json({
                        "message": "Company not found",
                    });
                }

                // Company exists, get the ID
                const companyId = companyResults[0].id;

                // Insert a new job entry into the Jobs table
                const insertQuery = `
                    INSERT INTO jobs (title, description, url, status, min_pay, max_pay, company_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                `;
                dbConnection.query(insertQuery, 
                    [data.title, data.description, data.url, data.status, data.min_pay, data.max_pay, companyId], 
                    (insertErr, insertResult) => {
                        if (insertErr) {
                            return res.status(400).json({
                                "message": insertErr.sqlMessage || "Failed to insert job.",
                                "error": insertErr
                            });
                        }

                        if (insertResult.affectedRows == 1) {
                            res.status(201).json({
                                "message": "Job inserted successfully",
                                "jobId": insertResult.insertId
                            });
                        } else {
                            throw new Error("No rows affected. Failed to insert job.");
                        }
                    });
            });
        });
    } catch (err) {
        console.log("**ERROR:", err.message);
        res.status(400).json({
            "message": err.message,
            "jobId": -1
        });
    }
};
