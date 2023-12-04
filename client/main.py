# Client-side python app

import requests  # calling web service
import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import sys
import os
import base64

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img

import client_functions as cf

import client_employer as ef




###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => check stats")
  print("   2 => check users")
  print("   3 => check jobs")
  print("   4 => job description extraction")
  print("   5 => check student&job match")
  print("   6 => bucket contents")
  print("   7 => Employer: add job")
  print("   8 => Employer: add company")
  print("   9 => Employer: change job status")

  cmd = int(input())
  return cmd


#########################################################################
# main
#
print('** Welcome to PhotoApp v2 **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'local-client-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (local-client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get('client', 'webservice')
apigatewayurl = configur.get('api_gateway', 'webservice')

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    cf.stats(baseurl)
  elif cmd == 2:
    cf.users(baseurl)
  elif cmd == 3:
    cf.assets(baseurl)
  elif cmd == 4:
    cf.job_description_extraction(apigatewayurl)
  elif cmd == 5:
    cf.student_job_matching(apigatewayurl)
  elif cmd == 6:
    cf.bucket_contents(baseurl)
  elif cmd == 7:
    ef.add_job(baseurl)
  elif cmd == 8:
    ef.add_company(baseurl)
  elif cmd == 9:
    ef.change_status(baseurl)
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
