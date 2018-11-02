#!/usr/bin/env python3
import sys
import json
import requests
import argparse
import signal
import multiprocessing.dummy as mp 
from random import randint

######## CHANGE THESE  (Or use `--email` and `--password` arguments) #########
USER_EMAIL = "email@example.com"
USER_PASSWORD = "password"
##############################################################################

# general args var instead of using multiple vars
global args

# COLORS !!
RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

# Safely stop the loops in case of CTRL+C
global interrputed
interrputed = False

# CTRL+C handling
def signal_handler(sig, frame):
    print(BLUE + '\n [*] You pressed Ctrl+C!')
    interrputed = True
    sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)


# In case the ZoomEye API URL ever changes
API_URL = "https://api.zoomeye.org"  




# Random UA since its required
def getRandomUserAgent():
    user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]
    return user_agents[randint(0, len(user_agents) - 1)]


def getToken():
    print(BLUE + "[*] Logging in as "+args.email)
    headers = {
        'User-Agent': getRandomUserAgent()
    }

    USER_DATA = '{"username": ' + '"' + args.email + '"' + \
                ', "password":  ' + '"' + args.password + '"' + '}'
    
    AUTH_REQUEST = requests.post(API_URL + '/user/login', data=USER_DATA, headers=headers) 

    try:
        # Wrong credentials
        if(AUTH_REQUEST.status_code == 403):
            raise KeyError

        ACCESS_TOKEN = AUTH_REQUEST.json()['access_token']
        print(GREEN + "[+] Successfuly logged in")
        return ACCESS_TOKEN
    except KeyError:
        print(RED + "[-] Invalid Credentials, please specify an email and password either in this file or with `--email` and `--password` arguments")
        quit()


def detectSaveMode():
    if args.save:
        print(BLUE + "[*] You have enabled save. All IPs will be saved to "+ args.save)
        try:
            global resultsFile
            # Append file instead of replacing it
            resultsFile = open(args.save, 'a')
        except:
            print(
                RED + "[-] Could not write to " + args.save + ", please check your permissions")
            quit()


def getPage(page):
    # This is the prefixed Token
    global TOKEN
    if(not args.save):
        print(BLUE + "[*] Parsing page: "+ str(page))
    else:
        # to keep the stdout clean
        print(BLUE + "[*] Parsing page: " + str(page), end='\r')
    
    # Moved HEADERS and SEARCH since they are'nt really global

    # Add the prefixed token to the headers, and the user agent
    HEADERS = {"Authorization": TOKEN, "user-agent": getRandomUserAgent()}

    SEARCH = requests.get(API_URL + '/' + args.platform + '/search',
                          headers=HEADERS, params={"query": args.query, "page": page})
    response = json.loads(SEARCH.text)
    i = 0
    try:
        global output
        while i < len(response["matches"]):
            if(interrputed): break
            if args.platform == "host":
                if args.port:
                    resultItem = response["matches"][i]["ip"] + ":" + \
                        str(response["matches"][i]["portinfo"]["port"])
                else:
                    resultItem = response["matches"][i]["ip"]

            elif args.platform == "web":
                if args.domain:
                    resultItem = response["matches"][i]["site"]
                else:
                    resultItem = response["matches"][i]["ip"][0]

            # output array
            output.append(resultItem)

            # clear the current line and print the result
            if not args.save:
                sys.stdout.write("\033[K")
                print(ENDC + resultItem)
            i += 1
    except IndexError:
        return
    except KeyError:
        print(RED + "[-] No hosts found")
        ipCount()
        quit()


# Loopy loop or multithread
def getResult():
    # same output array
    global output
    output = []

    # Get the token, once
    global TOKEN
    TOKEN = "JWT " + getToken()

    # Basic multithreading, save required
    if args.multi and args.save:
        p = mp.Pool(10)
        p.map(getPage, range(1, args.pages+1))
    else:
        currentPage = 1
        while currentPage <= args.pages:
            if(interrputed): break
            getPage(currentPage)
            currentPage += 1
    if args.save:
        global resultsFile
        resultsFile.writelines(["%s\n" % item  for item in output])

    


def ipCount():
    global output
    print(GREEN + "[+] " + str(len(output)) + " IPs saved to results.txt")


def main():
    parser = argparse.ArgumentParser(
        description='Simple ZoomEye searcher, outputs IPs to stdout or file')

    parser.add_argument("-q", "--query", help="Your ZoomEye Search")
    parser.add_argument(
        "-m", "--multi", help="enable multithreading", action="store_true")
    parser.add_argument(
        "-p", "--pages", help="Number of pages to search (Default: 5)", type=int, default=5)
    parser.add_argument(
        "--email", help="Your ZoomEye email", default=USER_EMAIL)
    parser.add_argument(
        "--password", help="Your ZoomEye password", default=USER_PASSWORD)
    parser.add_argument(
        "-s", "--save", help="Save output to <file>, default file name: results.txt", nargs="?", type=str, const="results.txt")
    parser.add_argument("-pl", "--platform",
                        help="Platforms to search, accepts \"host\" and \"web\" (Default: host)", default="host")
    parser.add_argument(
        "--port", help="Include the port number in the results (e.g., 127.0.0.1:1337) (Only for host platform)", action="store_true")
    parser.add_argument(
        "--domain", help="Output the site address rather than the IP. (Only for web platform)", action="store_true")
    global args
    args = parser.parse_args()


    detectSaveMode()
    getResult()
    ipCount()

    # The end
    print(ENDC)


if __name__ == '__main__':
    main()