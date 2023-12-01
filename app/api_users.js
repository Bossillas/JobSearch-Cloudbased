//
// app.get('/users', async (req, res) => {...});
//
// Return all the users from the database:
//
const dbConnection = require('./database.js')

exports.get_users = async (req, res) => {

  console.log("call to /users...");

  try {

    //
    // build input object with request parameters:
    //


    //
    // calling S3 to get bucket status, returning a PROMISE
    // we have to wait on eventually:
    //




    //
    // calling RDS to get # of users and # of assets. For 
    // consistency, we turn the DB call with callback into
    // a PROMISE so we can wait for it while we wait for
    // the S3 response:
    //
    var rds_response = new Promise((resolve, reject) => {
      try {
        console.log("/stats: calling RDS...");

        var sql = `
          WITH cte_skill_concat AS (
            SELECT 
              students.id AS id, 
              students.lastname AS lastname, 
              students.firstname AS firstname,
              students.email AS email, 
              students.linkedin AS linkedin, 
              schools.name AS schoolName,
              majors.major AS major,
              GROUP_CONCAT(skills.skill SEPARATOR ', ') AS skills
            FROM students
            JOIN schools 
              ON students.school_id = schools.id
            JOIN student_major sm
              ON students.id = sm.student_id
            JOIN majors 
              ON majors.id = sm.major_id
            JOIN student_skill ss 
              ON students.id = ss.student_id
            JOIN skills 
              ON skills.id = ss.skill_id
            GROUP BY students.id, students.lastname, students.firstname, students.email, students.linkedin, schools.name, majors.major
            ORDER BY students.id ASC
          )
          SELECT 
            id, 
            lastname, 
            firstname,
            email, 
            linkedin, 
            schoolName,
            GROUP_CONCAT(major SEPARATOR ', ') AS majors,
            skills
          FROM cte_skill_concat
          GROUP BY id, lastname, firstname, email, linkedin, schoolName, skills
          ORDER BY id ASC;
          `;


        dbConnection.query(sql, (err, results, _) => {
          try {
            if (err) {
              reject(err);
              return;
            }

            console.log("/stats query done");
            resolve(results);
          }
          catch (code_err) {
            reject(code_err);
          }
        });
      }
      catch (code_err) {
        reject(code_err);
      }
    });

    //
    // nothing else to do, so let's asynchronously wait
    // for the promises to resolve / reject:
    //
    Promise.all([rds_response]).then(results => {
      try {
        // we have a list of results, so break them apart:
        //var s3_result = results[0];
        //var rds_results = results[0];
        //console.log(rds_results);
        const data = results;
        console.log(results[0][0]);
        //console.log(results[0][0]["assetid"]);
        console.log(results[0].length);


        const extractedData = [];
        console.log("start");
        for (let i = 0; i < results[0].length; i++) {
          //const item = data[i];
          const item = results[0][i];
          console.log(item);
          console.log("next");
          const { id, lastname, firstname, email, linkedin, schoolName, majors, skills } = item;
          extractedData.push({
            //index: i, // Starting from 0
            id,
            lastname,
            firstname,
            email,
            linkedin,
            schoolName,
            majors,
            skills
          });
        }

        console.log(extractedData);

        console.log("/stats done, sending response...");

        res.json({
          "message": "success",
          "data": extractedData
        });
      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "data": -1
        });
      }
    }).catch(err => {
      //
      // we get here if calls to S3 or RDS failed, or we
      // failed to process the results properly:
      //
      res.status(400).json({
        "message": err.message,
        "data": []
      });
    });

  }//try
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get
