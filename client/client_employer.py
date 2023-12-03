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

class Company:
  id: int  # these must match columns from DB table
  name: str
  industry_id: int
  location: str
  industry: str

class Job:
  job_id: int  # these must match columns from DB table
  title: str
  description: str
  url: str
  status: str
  min_pay: int
  max_pay: int
  company_name: str

###################################################################
#
# add_company
#
def add_company(baseurl):
  """
  Prompts the user for adding company details
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  print("Enter company name>")
  name = input()

  print("Enter company industry>")
  industry = input()

  print("Enter company location>")
  location = input()


  try:
    #
    # build the data packet:
    #
    data = {
    "name": name,
    "industry": industry,
    "location": location
    }
    

    #
    # call the web service:
    #
    api = '/company'
    url = baseurl + api

    res = requests.put(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      print("reach here")
      # failed due to industry not found:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      body = res.json()
      print("Error message:", body["message"])
      if res.status_code == 404:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
        if body["message"] == "Industry not found":
            print("No worries, we will help you create industry profile first.")
            print("-----------------------------------------------------------")
            industry_data = {
            "industry": industry
            }
            api = '/industry'
            url = baseurl + api

            res = requests.put(url, json=industry_data)
            if res.status_code != 200:
                body = res.json()
                print("Error message:", body["message"])
                return
            body = res.json()

            userid = body["industryId"]
            message = body["message"]
            print("Industry:", industry, "with id:", userid, "is successfully inserted.")
            # re-try adding company
            api = '/company'
            url = baseurl + api

            res = requests.put(url, json=data)
            if res.status_code != 200:
                body = res.json()
                print("Error message:", body["message"])
                return

      # failed for other reason
      else:
        body = res.json()
        print("Error message:", body["message"])
        return


    #
    # success, extract userid:
    #
    body = res.json()

    userid = body["companyId"]
    message = body["message"]
    print(message)

    print(name, "with Company id:", userid, "is successfully inserted")

  except Exception as e:
    logging.error("add_company() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  

###################################################################
#
# add_company
#
def add_job(baseurl):
  """
  Prompts the user for adding job details
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  print("Enter company name>")
  company_name = input()

  print("Enter job title>")
  title = input()

  print("Enter job description local file name>")
  description = input()

  print("Enter job url>")
  url = input()

  print("Enter job min pay (please input the annual min base salary in integer format)>")
  min_pay = int(input())

  print("Enter job max pay (please input the annual min base salary in integer format)>")
  max_pay = int(input())


  try:
    #
    # build the data packet:
    #
    data = {
    "company_name": company_name,
    "title": title,
    "description": description,
    "url": url,
    "status": "open",
    "min_pay": min_pay,
    "max_pay": max_pay
    }
    

    #
    # call the web service:
    #
    api = '/job'
    url = baseurl + api

    res = requests.post(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 201:
      print("reach here")
      # failed due to industry not found:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      body = res.json()
      #print("Error message:", body["message"])
      if res.status_code == 404:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
        if body["message"] == "Company not found":
            print("Please go ahead and create your company profile first.")
            print("-----------------------------------------------------------")
            
            return
      if res.status_code == 409:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
        if body["message"] == "Job with the given URL already exists":
            print("You have already created this job with job id =",body["jobId"]),"No further action needed."
            print("-----------------------------------------------------------")
            return

      # failed for other reason
      else:
        body = res.json()
        print("Error message:", body["message"])
        return


    #
    # success, extract userid:
    #
    body = res.json()

    userid = body["jobId"]
    message = body["message"]
    print(message)

    print("Job id", userid, "is successfully created.")

  except Exception as e:
    logging.error("add_company() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return