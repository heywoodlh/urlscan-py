##urlscan-py

## Description:

Urlscan-py is a Python wrapper for urlscan.io's API to scan URLs.


## Requirements:

- Python3


## Installation and Usage:

Edit the urlscan_api variable in urlscan to equal a valid urlscan.io API key.


#### Begin a scan:

`./urlscan --url https://google.com`

The resulting output will produce a UUID. The UUID will be needed in order to retrieve the scan results. The output will also indicate whether the scan was successfully started or not.


#### Retrieve the scan results:

`./urlscan --retrieve UUID`

Following the `--retrieve` argument should be the UUID of the previously submitted scan.


#### Help syntax:

```
./urlscan -h

usage: urlscan [-h] [--url URL] [--retrieve RETRIEVE]

Wrapper for urlscan.io API

optional arguments:
  -h, --help           show this help message and exit
  --url URL            --url google.com
  --retrieve RETRIEVE  --retrieve UUID
```


## To do:

1. Cache history of retrieved scans in JSON file located in ~/.urlscan/history.

2. Add functionality to sort/filter through retrieved scans.
