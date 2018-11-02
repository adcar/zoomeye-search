# zoomeye-search

zoomeye-search is a standalone, lightweight python script for fetching IPs from ZoomEye search results.

## Prerequisites

* Python 3.x
* requests (`pip install requests`)

## Install

```
git clone https://github.com/MD5HashBrowns/zoomeye-search.git
cd zoomeye-search
./zoomeye.py -h
```

## ZoomEye Credentials

To specify your ZoomEye credentials within zoomeye-search, you can edit `zoomeye.py` and edit the lines that say "CHANGE THESE". Alternatively, you can provide your email and password with `--email` and `--password` arguments.

## Usage

```
$ ./zoomeye.py -h
```

```
usage: zoomeye.py [-h] [-q QUERY] [-m] [-p PAGES] [--email EMAIL]
                  [--password PASSWORD] [-s [SAVE]] [-pl PLATFORM] [--port]
                  [--domain]

Simple ZoomEye searcher, outputs IPs to stdout or file

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Your ZoomEye Search
  -m, --multi           enable multithreading
  -p PAGES, --pages PAGES
                        Number of pages to search (Default: 5)
  --email EMAIL         Your ZoomEye email
  --password PASSWORD   Your ZoomEye password
  -s [SAVE], --save [SAVE]
                        Save output to <file>, default file name: results.txt
  -pl PLATFORM, --platform PLATFORM
                        Platforms to search, accepts "host" and "web"
                        (Default: host)
  --port                Include the port number in the results (e.g.,
                        127.0.0.1:1337) (Only for host platform)
  --domain              Output the site address rather than the IP. (Only for
                        web platform)
```

## Output

### -s / --save option

Default: results.txt
```
$ ./zoomeye.py -p 1 -pl "web" -q app:wordpress -s
```

Or: 
```
$ ./zoomeye.py -p 1 -pl "web" -q app:wordpress -s file.txt
```


```
[*] You have enabled save. All IPs will be saved to results.txt
[*] Logging in as its.r@email.com
[+] Successfuly logged in
[+] 100 IPs saved to results.txt


```

### --port option

You can also tell zoomeye-search to include port numbers in the results. (This will work for shell redirection or `--save`)

```
$ ./zoomeye.py -p 1 "IIS"  --port
```

```
203.160.176.142:9030
203.81.110.91:9030
203.99.232.61:9030
203.115.31.75:9030
203.112.212.126:9030
203.154.236.12:9030
203.239.190.23:9030
203.142.136.52:9030
203.236.215.250:9030
203.44.6.229:9030
111.93.9.77:100
111.93.139.140:100
111.93.11.106:100
111.93.27.203:100
111.93.20.249:100
111.93.14.243:100
111.93.0.146:100
111.68.51.133:100
192.198.241.150:32400
12.18.174.234:7479
```
### --multi / -m option

You can enable multithreading for faster parsing, file output required.

```
$ ./zoomeye.py -p 1 -q app:wordpress --multi -s
```