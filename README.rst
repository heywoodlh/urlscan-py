##urlscan-py

## Description:

Urlscan-py is a Python wrapper for urlscan.io's API to scan URLs.



## Requirements:

- python3
- python3-pip



## Installation and Usage:

Via PyPI:

`sudo pip3 install urlscan-py`


### Saving the API key:

The API key will be stored in the default database that stores all initiated scan results. By default, this database is in `~/.urlscan/urlscan.db`. 

To save the API key, use the `init` command:

`urlscan init --api_key xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

If the API key is entered incorrectly or some other error occurs in which the API key value in the database is incorrect, either attempt to overwrite it with the above init command or remove the database file with this command: `rm ~/.urlscan/urlscan.db`.


### Scanning:

`urlscan scan --url https://google.com`

The resulting output will produce a UUID. The UUID will be needed in order to retrieve the scan results. The output will also indicate whether the scan was successfully started or not.

The `--url` flag can accept more than one URL at a time.


#### Save scan queue UUID results to different database file:

`urlscan scan --url https://google.com --db mydatabase.db`

This would allow the user to easily review the UUIDs of previously queued scans in an sqlite3 database. This defaults to a file named '.urlscaurlscan.db' if no other database file is specified.


#### Scan multiple domains stored in file 'example-domains.txt'

`urlscan scan --url * --file 'example-domains.txt'`

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



### Retrieve the scan results:

`urlscan retrieve --uuid UUID`

This will print the scan with the associated UUID to STDOUT. The `--uuid` flag can accept more than one UUID at a time.


#### Save retrieved results to specific directory:

`urlscan retrieve --uuid UUID --dir DIRECTORY`

By default, scans will be saved to the directory `.urlscasaved_scans`. Change this by using the `--dir` flag and specifying a different directory.


#### Save screenshot file:

`urlscan retrieve --uuid UUID --png`

The downloaded screenshot png will be stored in the default `--dir` directory which is `.urlscasaved_scans`. Specify a different `--dir` location to save the png to another directory.


#### Save dom file:

`urlscan retrieve --uuid UUID --dom`

The downloaded dom file will be stored in the default `--dir` directory which is `.urlscasaved_scans`. Specify a different `--dir` location to save the dom file to another directory. 



#### Retrieve command help:

```
urlscan retrieve --help

usage: urlscan retrieve [-h] --uuid UUID [UUID ...] [--db FILE] [--api KEY]
                           [-d DIRECTORY] [--dom] [--png] [-q]
optional arguments:
  -h, --help            show this help message and exit
  --uuid UUID [UUID ...]
                        UUID(s) to retrieve scans for
  --db FILE             specify different database file to query
  --api KEY             urlscan API key
  -d DIRECTORY, --dir DIRECTORY
                        directory to save scans to
  --dom                 save dom file from retrieved result
  --png                 save screenshot as png
  -q, --quiet           suppress output

```


## To do:
