//
// app.get('/assets', async (req, res) => {...});
//
// Return all the assets from the database:
//
const dbConnection = require('./database.js')

exports.get_assets = async (req, res) => {
  console.log("call to /stats...");

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
          SELECT j.id, j.title, j.url, j.min_pay,j.max_pay,c.name,c.industry_id,c.location
          FROM jobs j
          join companies c
          on j.company_id = c.id
          where j.status = 'open'
          ORDER BY j.id asc;
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

        

        const extractedData = [];

        for (let i = 0; i < results[0].length; i++) {
          //const item = data[i];
          const item = results[0][i];

          // Extract columns as per your SQL query
          const { id, title, url, min_pay, max_pay, name, industry_id, location } = item;
          extractedData.push({
            jobId: id,
            jobTitle: title,
            jobUrl: url,
            minPay: min_pay,
            maxPay: max_pay,
            companyName: name,
            industryId: industry_id,
            companyLocation: location
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
        "data": -1
      });
    });

  }//try
  catch (err) {
    //
    // generally we end up here if we made a 
    // programming error, like undefined variable
    // or function:
    //
    res.status(400).json({
      "message": err.message,
      "data": []
    });
  }//catch

  
}//get
