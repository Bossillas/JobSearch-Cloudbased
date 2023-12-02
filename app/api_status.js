const dbConnection = require('./database.js');

exports.post_status = async (req, res) => {
    console.log("call to /put-status...");

    try {
        const { job_id, new_status } = req.body;

        // Check if the job_id is provided
        if (!job_id || !new_status) {
            return res.status(400).json({ "message": "Job ID and new status are required" });
        }

        // Check if the job exists
        dbConnection.query('SELECT id FROM jobs WHERE id = ?', [job_id], (err, results) => {
            if (err) {
                return res.status(500).json({
                    "message": "Error querying the job",
                    "error": err
                });
            }

            if (results.length === 0) {
                return res.status(404).json({ "message": "Job not found" });
            }

            // Update the job status
            const updateQuery = 'UPDATE jobs SET status = ? WHERE id = ?';
            dbConnection.query(updateQuery, [new_status, job_id], (updateErr, updateResult) => {
                if (updateErr) {
                    return res.status(500).json({
                        "message": "Error updating the job status",
                        "error": updateErr
                    });
                }

                if (updateResult.affectedRows == 1) {
                    console.log("/put-status: job status updated...");
                    res.json({ "message": "Job status updated successfully" });
                } else {
                    throw new Error("No rows affected. Failed to update job status.");
                }
            });
        });
    } catch (err) {
        console.log("**ERROR:", err.message);
        res.status(400).json({
            "message": "Server error",
            "error": err
        });
    }
};
