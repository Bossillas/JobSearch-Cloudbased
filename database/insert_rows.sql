-- create initial data for the database

USE jobsearch;

INSERT INTO schools(name)
    values("Northwestern University"),
    values("Stanford University"),
    values("University of Chicago"),
    values("Harvard University"),
    values("University of Southern California");

INSERT INTO students(firstname, lastname, email, linkedin, resume_s3, school_id)
    values("boss", "paspanthong", "boss@nu.edu", "https://www.linkedin.com/in/bossy/", "b65e6881-2296-4264-b7f4-4d51562c5874", 1),
    values("juicy", "li", "juicy@nu.edu", "https://www.linkedin.com/in/juicy/", "3d59244a-d09e-4d4b-886f-f442b1811478", 1),
    values("cindy", "chen", "cindy@gmail.com", "https://www.linkedin.com/in/cindy/", "4ad7582b-117b-4627-97e5-c9d242ffd849", 1),
    values("ruben", "dias", "rdias@harvard.edu", "https://www.linkedin.com/in/rudendias/", "2ad43ac8-1008-48dd-965d-5fbbb56484cf", 4),
    values("chicago", "boi", "cboi@hotmail.com", "https://www.linkedin.com/in/chicagoboi/", "1d84da07-4492-4ebf-bc84-c6dbecf761f7", 3);

INSERT INTO majors(major)
    values("Industrial Engineering"),
    values("Computer Science"),
    values("Economics"),
    values("Business"),
    values("Mathematics"),
    values("Statistics"),
    values("Data Science"),
    values("Electrical Engineering");

INSERT INTO student_major(student_id, major_id)
    values(1, 1),
    values(1, 3),
    values(2, 6),
    values(3, 2),
    values(3, 7),
    values(4, 8),
    values(5, 4);

INSERT INTO skills(skill)
    values("Python"),
    values("R"),
    values("AWS"),
    values("Docker"),
    values("NodeJS"),
    values("GCP"),
    values("Azure"),
    values("Excel");

INSERT INTO student_skill(student_id, skill_id)
    values(1, 1),
    values(1, 3),
    values(1, 8),
    values(2, 2),
    values(3, 3),
    values(3, 6),
    values(3, 7),
    values(4, 5),
    values(5, 1),
    values(5, 4);

INSERT INTO industries(industry)
    values("E-commerce"),
    values("Finance"),
    values("Transportation"),
    values("Manufacturing"),
    values("Energy"),
    values("Healthcare"),
    values("Insurance");

INSERT INTO companies(name, industry_id, location)
    values("Capital One", 2, "McLean, VA"),
    values("Shopee", 1, "Singapore"),
    values("NationWide", 7, "Remote, USA")
    values("UPS", 3, "Atlanta, GA");

INSERT INTO jobs(title, description, url, status, min_pay, max_pay, company_id)
    values("Data Scientist", "2efc208e-1b73-462d-8e57-2f44b13d2dda", "https://www.capitalone.com/careers/R1234", "open", 100000, 150000, 1),
    values("Principal Data Scientist", "696162b6-e5b5-4074-865e-2c34a27278d9", "https://www.capitalone.com/careers/R5436", "closed", 150000, 200000, 1),
    values("Data Analyst", "528b4f01-8da5-48a7-b2ce-05a86e46e415", "https://www.shopee.com/careers/R13564", "open", 45000, 60000, 2),
    values("Full Stack Developer", "68dda80a-1f07-4c83-8872-b34036f2ed9b", "https://www.nationwide.com/careers/rt45264", "closed", 80000, 100000, 3),
    values("VP Marketing", "3e910e20-d07d-4a5f-93a4-be9a92fa108a", "https://www.ups.com/careers/7249305", "open", 250000, 400000, 4);
