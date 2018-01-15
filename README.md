##urlscan-py

## Description:

Urlscan-py is a Python wrapper for urlscan.io's API to scan URLs.


## Requirements:

- Python3


## Installation and Usage:

`git clone https://github.com/heywoodlh/urlscan-py`

`cd urlscan-py`

`sudo pip3 install -r requirements.txt`

Edit the urlscan_api variable in urlscan.py to equal a valid urlscan.io API key.


### Scanning:

`./urlscan.py scan --url https://google.com`

The resulting output will produce a UUID. The UUID will be needed in order to retrieve the scan results. The output will also indicate whether the scan was successfully started or not.

The `--url` flag can accept more than one URL at a time.

#### Save scan queue UUID results to different database file:

`./urlscan.py scan --url https://google.com --db mydatabase.db`

This would allow the user to easily review the UUIDs of previously queued scans in an sqlite3 database. This defaults to a file named '~/.urlscan/urlscan.db' if no other database file is specified.

#### Scan multiple domains stored in file 'example-domains.txt'

`./urlscan.py scan --url * --file 'example-domains.txt'`

Each domain should be stored in a file with each domain separated by a newline

#### Scan command help:

```
./urlscan.py scan --help

usage: urlscan.py scan [-h] --url URL [URL ...] [-s FILE] [-f FILE] [-q]

optional arguments:
  -h, --help            show this help message and exit
  --url URL [URL ...]   URL(s) to scan
  --db FILE             specify different database file initiated scans 
                        will be saved to
  -f FILE, --file FILE  file with url(s) to scan
  -q, --quiet           suppress output

```



### Retrieve the scan results:

`./urlscan.py retrieve --uuid UUID`

This will print the scan with the associated UUID to STDOUT. The `--uuid` flag can accept more than one UUID at a time.

#### Save retrieved results to directory:

`./urlscan.py retrieve --uuid UUID --dir DIRECTORY`

By default, scans will be saved to a directory called saved_scans in the same folder. Change this by using the `--dir` flag and specifying a different directory.


#### Retrieve command help:

```
./urlscan.py retrieve --help

usage: urlscan retrieve [-h] --uuid UUID [UUID ...] [-s] [-d DIRECTORY] [-q]

optional arguments:
  -h, --help            show this help message and exit
  --uuid UUID [UUID ...]
                        UUID(s) to retrieve scans for
  -d, --dir DIRECTORY
                        directory to save scans to
  -q, --quiet           suppress output
```


## To do:

1. Add functionality to sort/filter through retrieved scans.
2. Store the UUIDs from the submission in a local database (sqlite)
3. Periodically poll the urlscan.io API to see if a scan is finished
4. If it's finished, download the API reply, the screenshot and the DOM
5. Provide an additional option to also attempt to download the response
  files.
