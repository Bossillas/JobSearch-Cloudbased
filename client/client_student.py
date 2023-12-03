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
    