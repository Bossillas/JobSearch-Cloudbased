# JobSearch-Cloudbased

## Project Structure
```
project_root/
├── app/
│   ├── api_assets.js
│   ├── api_company.js
│   ├── api_industry.js
│   ├── api_jd.js
│   ├── api_job.js
│   ├── api_major.js
│   ├── api_resume.js
│   ├── api_school.js
│   ├── api_skill.js
│   ├── api_status.js
│   ├── api_stats.js
│   ├── api_student.js
│   ├── aws.js
│   ├── app.js
│   └── config.js
│   └── database.js
├── client/
│   ├── client_employer.py
│   ├── client_functions.py
│   ├── client_student.py
│   └── main.py
├── database/
│   ├── create_access.sql
│   ├── create_database.sql
│   └── insert_rows.sql
└── lambda_functions/
    ├── jd_extract/
    │   ├── lambda_function.py
    │   ├── datatier.py
    │   └── config.ini
    └── student_job_matching/
        ├── lambda_function.py
        ├── datatier.py
        └── config.ini
```


## app folder (JavaScript Code)
index.js
config.js
aws.js
database.js

### GET APIs
- api_assets.js: Return all the job related information from job/company/industry tables
    
    jobId, jobTitle, jobUrl, minPay, maxPay, companyName, industry, companyLocation

- api_users.js: 
- api_stats.js

### PUT APIs
- api_company.js
- api_industry.js
- api_major.js
- api_school.js
- api_skill.js

### POST APIs
- api_job.js

## client folder

### Functions
- client_functions.py: general functions and calls to Lambda functions
- client_employer.py: 
- client_student.py: 

### App file
- main.py

## lambda_function folder
- jd_extract
- student_job_matching

## database folder