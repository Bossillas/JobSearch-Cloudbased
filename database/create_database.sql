CREATE DATABASE IF NOT EXISTS jobsearch;

USE jobsearch;

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS majors;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS schools;
DROP TABLE IF EXISTS student_major;
DROP TABLE IF EXISTS student_skill;

CREATE TABLE schools
(
    id          int not null AUTO_INCREMENT,
    name        varchar(128) not null,
    UNIQUE      (name)
);
ALTER TABLE schools AUTO_INCREMENT = 1;

CREATE TABLE students
(
    id          int not null AUTO_INCREMENT,
    firstname   varchar(64) not null,
    lastname    varchar(64) not null,
    email       varchar(128) not null,
    linkedin    varchar(256),
    resume_s3   varchar(256),
    school_id   int,
    PRIMARY KEY (id),
    UNIQUE      (email),
    UNIQUE      (linkedin),
    UNIQUE      (resume_s3),
    FOREIGN KEY (school_id) REFERENCES schools(id)
);
ALTER TABLE students AUTO_INCREMENT = 1;

CREATE TABLE majors
(
    id          int not null AUTO_INCREMENT,
    major      varchar(64) not null,
    PRIMARY KEY (id),
    UNIQUE      (major)
);
ALTER TABLE majors AUTO_INCREMENT = 1;

CREATE TABLE student_major
(
    student_id  int not null,
    major_id    int not null,
    PRIMARY KEY (student_id, major_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (major_id) REFERENCES majors(id)
);

CREATE TABLE skills
(
    id          int not null AUTO_INCREMENT,
    skill       varchar(64) not null,
    PRIMARY KEY (id),
    UNIQUE      (skill)
);
ALTER TABLE skills AUTO_INCREMENT = 1;

CREATE TABLE student_skill
(
    student_id  int not null,
    skill_id    int not null,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE industries
(
    id          int not null AUTO_INCREMENT,
    industry    varchar(64) not null,
    PRIMARY KEY (id),
    UNIQUE      (industry)
);
ALTER TABLE industries AUTO_INCREMENT = 1;

CREATE TABLE companies
(
    id          int not null AUTO_INCREMENT,
    name        varchar(128) not null,
    industry_id int not null,
    location    varchar(256) not null,
    PRIMARY KEY (id),
    UNIQUE      (name),
    UNIQUE      (location),
    FOREIGN KEY (industry_id) REFERENCES industries(id)
);
ALTER TABLE companies AUTO_INCREMENT = 1;

CREATE TABLE jobs
(
    id          int not null AUTO_INCREMENT,
    title       varchar(128) not null,
    description varchar(16384) not null,
    url         varchar(256) not null,
    status      varchar(64) not null,
    min_pay     int,
    max_pay     int,
    company_id  int not null,
    PRIMARY KEY (id),
    UNIQUE      (url),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
ALTER TABLE jobs AUTO_INCREMENT = 1;