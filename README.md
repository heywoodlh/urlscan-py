## urlscan-py

## Description:

Urlscan-py is a Python wrapper for urlscan.io's API to scan URLs.


## Installation and Usage:

### Using the Docker image:

`docker pull heywoodlh/urlscan-py`

See the [Docker Readme](https://github.com/heywoodlh/urlscan-py/blob/master/docker/README.md) for a few simple examples on how to use the image.


### Installation Via PyPI:

`pip3 install --user urlscan-py`


### Saving the API key:

The API key will be stored in the default database that stores all initiated scan results. By default, this database is in `~/.urlscan/urlscan.db`.

To save the API key to a local database, use the `init` command:

`urlscan init --api xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

If the API key is entered incorrectly or some other error occurs in which the API key value in the database is incorrect, either attempt to overwrite it with the above init command or remove the database file with this command: `rm ~/.urlscan/urlscan.db`.


### Scanning:

`urlscan scan --url https://google.com`

The resulting output will produce a UUID. The UUID will be needed in order to retrieve the scan results. The output will also indicate whether the scan was successfully started or not.

The `--url` flag can accept more than one URL at a time.


#### Save scan queue UUID results to different database file:

`urlscan scan --url https://google.com --db mydatabase.db`

This would allow the user to easily review the UUIDs of previously queued scans in an sqlite3 database. This defaults to a file named `$HOME/.urlscan/urlscan.db` if no other database file is specified.


#### Scan multiple domains stored in file 'example-domains.txt'

`urlscan scan --file 'example-domains.txt'`

Each domain should be stored in a file with each domain separated by a newline.


#### Scan command help:

```
urlscan scan --help

usage: urlscan scan [-h] [--url URL [URL ...]] [--db FILE] [-f FILE] [-q]
                       [--api KEY]
optional arguments:
  -h, --help            show this help message and exit
  --url URL [URL ...]   URL(s) to scan
  --db FILE             specify different database file initiated scans will
                        be saved to
  -f FILE, --file FILE  file with url(s) to scan
  -q, --quiet           suppress output
  --api KEY             urlscan API key

```

### Searching for queued or previously completed scans

#### Search local database for all previously queued scans:

`urlscan search`


#### Search local database for previous scan:

`urlscan search --url example.com`


#### Search urlscan.io for public scans on a domain:

`urlscan search --url example.com --web`


#### Search command help:

```
$ urlscan search --help
usage: urlscan search [-h] [--url URL [URL ...]] [--db FILE] [--web]

optional arguments:
  -h, --help           show this help message and exit
  --url URL [URL ...]  url(s) to search for matching UUID
  --db FILE            specify different database file to search
  --web                search urlscan.io for URL (public)
```


### Retrieve the scan results:

`urlscan retrieve --uuid UUID`

This will print the scan with the associated UUID to STDOUT. The `--uuid` flag can accept more than one UUID at a time.


### Retrieve a summary of a scan:

`$ urlscan retrieve --uuid UUID --summary`

The results look similar to this:

```
Domain: example.domain
IP Address: xxx.xxx.xxx.xxx
Country: US
Server: nginx
Web Apps: ['Nginx']
Number of Requests: 3
Ads Blocked: 0
HTTPS Requests: 100%
IPv6: 0%
Unique Country Count: 1
Malicious: False
Malicious Requests: 0
Pointed Domains: ['example.domain']
```




#### Save retrieved results to specific directory:

`urlscan retrieve --uuid UUID --dir DIRECTORY`

By default, scans will be saved to the directory `.urlsaved_scans`. Change this by using the `--dir` flag and specifying a different directory.


#### Save screenshot file:

`urlscan retrieve --uuid UUID --png`

The downloaded screenshot png will be stored in the default `--dir` directory which is `~/.urlscan/saved_scans`. Specify a different `--dir` location to save the png to another directory.


#### Save dom file:

`urlscan retrieve --uuid UUID --dom`

The downloaded dom file will be stored in the default `--dir` directory which is `~/.urlscan/saved_scans`. Specify a different `--dir` location to save the dom file to another directory.



#### Retrieve command help:

```
$ urlscan retrieve --help

usage: urlscan retrieve [-h] --uuid UUID [UUID ...] [--db FILE] [--api KEY]
                           [-d DIRECTORY] [--dom] [--png] [-q]
optional arguments:
  -h, --help            show this help message and exit
  --uuid UUID [UUID ...]
                        UUID(s) to retrieve scans for
  --db FILE             specify different database file to query
  --api KEY             urlscan API key
  -s, --summary         print summary of result
  -d DIRECTORY, --dir DIRECTORY
                        directory to save scans to
  --dom                 save dom file from retrieved result
  --png                 save screenshot as png
  -q, --quiet           suppress output

```



Author: Spencer Heywood

Email: l.spencer.heywood@protonmail.com
