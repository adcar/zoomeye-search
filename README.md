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
usage: zoomeye.py [-h] [-p PAGES] [--email EMAIL] [--password PASSWORD] [-s]
                  [-pl PLATFORM] [--port]
                  search

Simple ZoomEye searcher, outputs IPs to stdout or file

positional arguments:
  search                Your ZoomEye Search

optional arguments:
  -h, --help            show this help message and exit
  -p PAGES, --pages PAGES
                        Number of pages to search (Default: 5)
  --email EMAIL         Your ZoomEye email
  --password PASSWORD   Your ZoomEye password
  -s, --save            Save output to results.txt
  -pl PLATFORM, --platform PLATFORM
                        Platforms to search, accepts "host" and "web"
                        (Default: host)
  --port                Include the port number in the results (e.g.,
                        127.0.0.1:1337) (Only for host platform)
```

## Output

### Shell Redirection:

By default, zoomeye-search.py will only output IPs. This allows for sending stdout to some other file with shell redirection.

```
$ ./zoomeye.py -p 1 port:123 >> somefile.txt
```

```
$ cat somefile.txt
62.80.176.164
62.42.37.3
62.133.141.88
62.90.77.101
62.12.27.55
62.215.181.164
62.73.84.64
62.182.13.143
62.233.188.41
62.117.128.180
```

### -s / --save option

```
$ ./zoomeye.py -p 1 -pl "web" app:wordpress -s
```

```
You have enabled save. All IPs will be saved to results.txt.

Page 1
98.138.19.143
194.63.248.47
45.34.23.170
77.243.131.33
80.237.132.71
98.129.229.68
143.95.38.203
192.185.241.151
104.24.125.81
89.38.254.66

10 IPs saved to results.txt.
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
