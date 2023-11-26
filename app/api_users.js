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
            select students.id as id, students.lastname as lastname,students.firstname as firstname,students.email as email,students.linkedin as linkedin,schools.name as schoolName
            from students
            join schools
            on students.school_id = schools.id
            order by students.id asc;
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
          const { id, email, lastname, firstname, linkedin, schoolName } = item;
          extractedData.push({
            //index: i, // Starting from 0
            id,
            email,
            lastname,
            firstname,
            linkedin,
            schoolName
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
