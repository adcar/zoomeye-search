#!/usr/local/bin/python3.6
import sys
import json
import requests
import argparse

######## CHANGE THESE  (Or use `--email` and `--password` arguments) #########
USER_EMAIL = "email@example.com"
USER_PASSWORD = "yourpassword"
##############################################################################



parser = argparse.ArgumentParser(description='Simple ZoomEye searcher, outs IPs to stdout or file')

parser.add_argument("search", help="Your ZoomEye Search")
parser.add_argument("-pg", "--pages", help="Number of pages to search (Default: 5)", type=int, default=5)
parser.add_argument("-e", "--email", help="Your ZoomEye email", default=USER_EMAIL)
parser.add_argument("-pw", "--password", help="Your ZoomEye password", default=USER_PASSWORD)
parser.add_argument("-s", "--save", help="Save output to results.txt", action="store_true")
args = parser.parse_args()

QUERY = args.search
PAGECOUNT = args.pages
EMAIL = args.email
PASSWORD = args.password

API_URL = "https://api.zoomeye.org" # In case the ZoomEye API URL ever changes

USER_DATA='{"username": ' + '"'+EMAIL+'"' + ', "password":  ' + '"'+PASSWORD+'"' + '}'
AUTH_REQUEST = requests.post(API_URL + '/user/login', data=USER_DATA)

# Attempts to access the raw token, if there is a KeyError it means the credentials are incorrect
try:
  ACCESS_TOKEN = AUTH_REQUEST.json()['access_token'];
except KeyError:
  print("[ERROR] Invalid Credentials, please specify an email and password either in this file or with `--email` and `--password` arguments")
  quit()
  
# This is the prefixed Token
TOKEN = "JWT " + ACCESS_TOKEN

# Add the prefixed token to the headers
HEADERS = {"Authorization": TOKEN}


if args.save:
  print("You have enabled save. All IPs will be saved to results.txt.")
  try:
    resultsFile = open('results.txt', 'w')
  except:
    print("[ERROR] Could not write to results.txt, please check your permissions")
    quit()
    
# Loopy loop
currentPage = 1
while currentPage <= PAGECOUNT:
  print("\nPage " + str(currentPage))
  SEARCH = requests.get(API_URL + '/host/search', headers=HEADERS, params={"query": QUERY, "page": currentPage})
  response = json.loads(SEARCH.text)
  i = 0
  try:
    while i < 10:
      print(response["matches"][i]["ip"])
      if args.save:
        resultsFile.write(response["matches"][i]["ip"] + "\n")
      
      i += 1
  except IndexError:
    break
  currentPage += 1



resultsFile.close() # Close as write
ip_count = sum(1 for line in open("results.txt", "r")) # Open as read


if args.save:
  print("\n" + str(ip_count) + " IPs saved to results.txt.")



