
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

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


###################################################################
#
# classes
#
class User:
  id: int  # these must match columns from DB table
  lastname: str
  firstname: str
  email: str
  linkedin: str
  schoolName: str
  majors: str
  skills: str


class Asset:
  jobId: int  # these must match columns from DB table
  jobTitle: str
  jobUrl: str
  minPay: int
  maxPay: int
  companyName: str
  industry: str
  companyLocation: str


class BucketItem:
  Key: str
  LastModified: str
  ETag: str
  Size: int
  StorageClass: str



###################################################################
# stats
def stats(baseurl):
  """
  Prints out S3 and RDS info: bucket status, # of users jobs, and companies in the database
  
  Parameters:
    baseurl: baseurl for web service
  Returns
    nothing
  """

  try:
    # call the web service:
    api = '/stats'
    url = baseurl + api

    res = requests.get(url)
    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    # deserialize and extract stats:
    body = res.json()
    #
    print("Status:", body["message"])
    print("Number of users:", body["db_numStudents"])
    print("Number of jobs:", body["db_NumJobs"])
    print("Number of companies:", body["db_NumCompanies"])

  except Exception as e:
    logging.error("stats() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
# users
def users(baseurl):
  """
  Prints out all the users in the database
  
  Parameters
    baseurl: baseurl for web service
  Returns
    nothing
  """

  try:
    # call the web service:
    api = '/users'
    url = baseurl + api

    res = requests.get(url)

    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    # deserialize and extract users:
    body = res.json()
    #
    # let's map each dictionary into a User object:
    #
    users = []
    for row in body["data"]:
      user = jsons.load(row, User)
      users.append(user)
    # Now we can think OOP:
    for user in users:
      print(user.id)
      print(" User:", user.lastname, ",", user.firstname)
      print(" Email:", user.email)
      print(" Linkedin:", user.linkedin)
      print(" School:", user.schoolName)
      print(" Majors:", user.majors)
      print(" Skills:", user.skills)

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
# Show all jobs info (assets api)
def assets(baseurl):
  """
  Prints out all the assets in the database
  
  Parameters
    baseurl: baseurl for web service
  Returns
    nothing
  """

  try:
    # call the web service:
    api = '/assets'
    url = baseurl + api

    res = requests.get(url)

    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    # deserialize and extract assets:
    body = res.json()
    # let's map each dictionary into an Asset object:
    assets = []
    for row in body["data"]:
      asset = jsons.load(row, Asset)
      assets.append(asset)
    # Now we can think OOP:
    for asset in assets:
      print("Job", asset.jobId)
      print(" Title:", asset.jobTitle)
      print(" Pay Range:", asset.minPay, "~", asset.maxPay)
      print(" Company:", asset.companyName)
      print(" Industry:", asset.industry)
      print(" Location:", asset.companyLocation)
      print(" Url:", asset.jobUrl)

  except Exception as e:
    logging.error("assets() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
# job_description_extraction
def job_description_extraction(baseurl):
  """
  Prompts the user for the job id, and provide user with the key word extraction result.

  Parameters
    baseurl: baseurl for web service
  Returns
    nothing
  """

  print("Enter job id>")
  jobid = input()
  print("It might takes about 10 seconds to run, please wait...")

  try:
    #
    # call the web service:
    #
    api = '/job_description_extraction'
    url = baseurl + api + '/' + jobid

    res = requests.get(url)

    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      return

    # extract results:
    body = res.json()
    # print(body)

    # Replace single quotes with double quotes, but first replace the inner single quotes in the lists
    body = body.replace("['", '[\"').replace("']", '\"]').replace("', '", '", "').replace("', \"", '", "').replace("\", '", '", "')
    # Now replace the outer single quotes
    body = body.replace("'", "\"")
    # Convert to dictionary
    body_dict = json.loads(body)

    print("** Job Description Keys: **")
    print('_________________________________________________________')
    print('- Provide sponsorship:', body_dict['provide sponsorship'])
    print('_________________________________________________________')
    print('- Security clearance requirements:', body_dict['security clearance'])
    print('_________________________________________________________')
    print('- Skills requirements:')
    skills_str = ''
    for s in body_dict['skills']:
      skills_str += s
      skills_str += ', '
    print(skills_str)
    print('_________________________________________________________')
    if body_dict['number of years of working experience'] == -1:
      print('- Number of years of working experience requirements: Not mentioned')
    else:
      print('- Number of years of working experience requirements:', body_dict['number of years of working experience'])
    print('_________________________________________________________')
    print('- Education background requirements:')
    edus_str = ''
    for e in body_dict['education background requirement']:
      edus_str += e
      edus_str += ', '
    print(edus_str)

    return

  except Exception as e:
    logging.error("job_description_extraction() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  

############################################################
# Student job matching
def student_job_matching(baseurl):
  """
  Prompts the user for the job id and student id, and provide user with student vs. job matching score.

  Parameters
    baseurl: baseurl for web service
  Returns
    nothing
  """

  print("Enter job id>")
  jobid = input()
  print("Enter user id>")
  studentid = input()
  print("It might takes about 10 seconds to run, please wait...")

  try:
    #
    # call the web service:
    #
    api = '/student_job_matching'
    url = baseurl + api + '/' + jobid + '/' + studentid

    res = requests.get(url)

    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      return

    # extract results:
    body = res.json()
    # print(body)

    # # Replace single quotes with double quotes, but first replace the inner single quotes in the lists
    # body = body.replace("['", '[\"').replace("']", '\"]').replace("', '", '", "').replace("', \"", '", "').replace("\", '", '", "')
    # # Now replace the outer single quotes
    # body = body.replace("'", "\"")
    # # Convert to dictionary
    body_dict = json.loads(body)

    print("** User VS. Job Matching: **")
    print('_________________________________________________________')
    print('Score:', body_dict['score'])
    print('_________________________________________________________')
    print('Strengths:')
    for s in body_dict['strengths']:
      print(" - ", s)
    print('_________________________________________________________')
    print('Areas for improvement:')
    for a in body_dict['areas_for_improvement']:
      print(' - ', a)
    return

  except Exception as e:
    logging.error("job_description_extraction() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

