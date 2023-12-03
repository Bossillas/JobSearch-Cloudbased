
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
#
# stats
#
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
#
# users
#
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







###################################################################
#
# download
#
def download(baseurl, display=False):
  """
  Prompts the user for an asset id, and downloads
  that asset (image) from the bucket. Displays the
  image after download if display param is True.
  
  Parameters
  ----------
  baseurl: baseurl for web service,
  display: optional param controlling display of image
  
  Returns
  -------
  nothing
  """

  print("Enter asset id>")
  assetid = input()

  try:
    #
    # call the web service:
    #
    api = '/download'
    url = baseurl + api + '/' + assetid

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract image:
    #
    body = res.json()

    #
    # did we get an image back? Perhaps asset id was invalid...
    #
    userid = body["user_id"]

    if userid == -1:
      # no such image
      print("No such asset...")
      return

    #
    # we have an image:
    #
    assetname = body["asset_name"]
    bucketkey = body["bucket_key"]

    print("userid:", userid)
    print("asset name:", assetname)
    print("bucket key:", bucketkey)

    bytes = base64.b64decode(body["data"])

    #
    # write the binary data to a file (as a
    # binary file, not a text file):
    #
    outfile = open(assetname, "wb")
    outfile.write(bytes)
    outfile.close()

    print("Downloaded from S3 and saved as '", assetname, "'")

    if display:  # display the image?
      image = img.imread(assetname)
      plt.imshow(image)
      plt.show()

  except Exception as e:
    logging.error("download() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# bucket_contents
#
def bucket_contents(baseurl):
  """
  Prints out the contents of the S3 bucket
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/bucket'
    url = baseurl + api

    #
    # we have to loop since data is returned page
    # by page:
    #
    while True:
      #
      res = requests.get(url)

      #
      # let's look at what we got back:
      #
      if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        print("url: " + url)
        if res.status_code == 400:  # we'll have an error message
          body = res.json()
          print("Error message:", body["message"])
        #
        return

      #
      # deserialize and extract bucket contents, note
      # that contents are coming back a page (12) at
      # a time...
      #
      body = res.json()

      #
      # let's map each dictionary into a BucketItem object:
      #
      items = []
      for row in body["data"]:
        item = jsons.load(row, BucketItem)
        items.append(item)

      #
      # do we have any data to display?
      #
      if len(items) == 0:
        # no
        break

      #
      # Now we can think OOP:
      #
      lastkey = None  # we have at least 1 asset, so this will get set

      for item in items:
        print(item.Key)
        print(" ", item.LastModified)
        print(" ", item.Size)
        lastkey = item.Key

      print("another page? [y/n]")
      answer = input()

      if answer == 'y':
        # add parameter to url
        url = baseurl + api
        url += "?startafter=" + lastkey
        #
        continue
      else:
        break

  except Exception as e:
    logging.error("bucket_contents() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# add_user
#
def add_user(baseurl):
  """
  Prompts the user for the new user's email,
  last name, and first name, and then inserts
  this user into the database.
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  print("Enter user's email>")
  email = input()

  print("Enter user's last (family) name>")
  last_name = input()

  print("Enter user's first (given) name>")
  first_name = input()

  # generate unique folder name:
  folder = str(uuid.uuid4())

  try:
    #
    # build the data packet:
    #
    data = {
      "email": email,
      "lastname": last_name,
      "firstname": first_name,
      "bucketfolder": folder
    }

    #
    # call the web service:
    #
    api = '/user'
    url = baseurl + api

    res = requests.put(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # success, extract userid:
    #
    body = res.json()

    userid = body["userid"]
    message = body["message"]

    print("User", userid, "successfully", message)

  except Exception as e:
    logging.error("add_user() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# upload
#
def upload(baseurl):
  """
  Prompts the user for a local filename and user id, 
  and uploads that asset (image) to the user's folder 
  in the bucket. The asset is given a random, unique 
  name. The database is also updated to record the 
  existence of this new asset in S3.
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  print("Enter local filename>")
  local_filename = input()

  if not pathlib.Path(local_filename).is_file():
    print("Local file '", local_filename, "' does not exist...")
    return

  print("Enter user id>")
  userid = input()

  try:
    #
    # build the data packet:
    #
    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()

    #
    # now encode the image as base64. Note b64encode returns
    # a bytes object, not a string. So then we have to convert
    # (decode) the bytes -> string, and then we can serialize
    # the string as JSON for upload to server:
    #
    data = base64.b64encode(bytes)
    datastr = data.decode()

    data = {"assetname": local_filename, "data": datastr}

    #
    # call the web service:
    #
    api = '/image'
    url = baseurl + api + "/" + userid

    res = requests.post(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # success, extract userid:
    #
    body = res.json()

    assetid = body["assetid"]

    print("Image uploaded, asset id =", assetid)

  except Exception as e:
    logging.error("upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

