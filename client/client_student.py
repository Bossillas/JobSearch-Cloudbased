import requests  # calling web service
import jsons  # relational-object mapping
import json

import uuid
import pathlib
import logging
import sys
import os
import base64
import pandas as pd

class Student:
    id: int
    firstname: str
    lastname: str
    email: str
    linkedin: str
    resume_s3: str
    school_id: int
    
def add_student(baseurl):
    
    print("Enter firstname>")
    firstname = input()
    
    print("Enter lastname>")
    lastname = input()
    
    print("Enter email>")
    email = input()
    
    print("Enter Linkedin URL>")
    linkedin = input()
    
    print("Enter school name>")
    school = input()
    
    print("Enter skills (type 0 to stop)>")
    skill = input()
    skills = []
    while skill != 0:
        skills.append(skill)
        print("Enter skills (type 0 to stop)>")
        skill = input()
        
    print("Enter majors (type 0 to stop)>")
    major = input()
    majors = []
    while major != 0:
        majors.append(major)
        print("Enter skills (type 0 to stop)>")
        major = input()
        
    print("Enter resume filename>")
    resume = input()
    
    # check if resume file exist
    if not pathlib.Path(resume).is_file():
        print("Local file '", resume, "' does not exist...")
        return
    
    # add skills & majors
    add_skills(baseurl, skills)
    add_majors(baseurl, majors)
    
    # add student
    url = baseurl + "/student"
    data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "linkedin": linkedin,
        "resume_s3": None,
        "school": school,
        "skill": skills,
        "major": majors
    }
    try:
        res = requests.put(url, json=data)
        if res.status_code != 200:
                # failed:
                print("Failed with status code:", res.status_code)
                print("url: " + url)
                if res.status_code == 400:  # we'll have an error message
                    body = res.json()
                    print("Error message:", body["message"])
                #
                return
    except Exception as e:
        logging.error("add_student() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return
    
    # get student id if success
    student_id = res.body["studentId"]
    
    # add resume
    add_resume(baseurl, resume, student_id)
    
    
def add_skills(baseurl, skills):
    
    url = baseurl + "/skill"
    
    for skill in skills:
        data = {"skill": skill}
        res = requests.put(url, json=data)
        
        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 400:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return
    
    print("Insert skills successfully!")
    
def add_majors(baseurl, majors):
    url = baseurl + "/skill"
    
    for major in majors:
        data = {"major": major}
        res = requests.put(url, json=data)
        
        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 400:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return
    
    print("Insert majors successfully!")
    
def add_resume(baseurl, local_filename, student_id):
    url = baseurl + "/resume/" + str(student_id)
    
    try:
        infile = open(local_filename, "rb")
        bytes = infile.read()
        infile.close()
        
        data = base64.b64encode(bytes)
        datastr = data.decode()
        
        data = {
            "data": datastr
        }
        
        # call api
        res = requests.post(url, json=data)
        if res.status_code != 200:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 400:  # we'll have an error message
                body = res.json()
                print("Error message:", body["message"])
            #
            return
        
        # success
        print("Resume uploaded, student id =", student_id)
    except Exception as e:
        logging.error("add_resume() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return