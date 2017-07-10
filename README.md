# zoomeye-search
Simple ZoomEye searcher written in Python 3.6. IPs can be exported as .txt


## Prerequisites
Python 3.x
## Install
```
git clone https://github.com/MD5HashBrowns/zoomeye-search.git
cd zoomeye-search
./zoomeye-search.py -h
```
## Usage
```
usage: zoomeye.py [-h] [-pa PAGES] [-e EMAIL] [-pw PASSWORD] [-s] [-pl PLATFORM] search

Simple ZoomEye searcher, outs IPs to stdout or file

positional arguments:
  search                Your ZoomEye Search

optional arguments:
  -h, --help            show this help message and exit
  -pa PAGES, --pages PAGES
                        Number of pages to search (Default: 5)
  -e EMAIL, --email EMAIL
                        Your ZoomEye email
  -pw PASSWORD, --password PASSWORD
                        Your ZoomEye password
  -s, --save            Save output to results.txt
  -pl PLATFORM, --platform PLATFORM
                        Platforms to search, accepts "host" and "web" (Default: host)
```
## Output
By default, zoomeye-search.py will only output IPs. This allows for sending stdout to some other file with shell redirection.
### Example:
```
chronos@localhost ~/Downloads/git/zoomeye-search $ ./zoomeye.py -pa 1 port:123 >> somefile.txt
chronos@localhost ~/Downloads/git/zoomeye-search $ cat somefile.txt 
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
chronos@localhost ~/Downloads/git/zoomeye-search $ 
```
