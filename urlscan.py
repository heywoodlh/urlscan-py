#!/usr/bin/env python3
import argparse
import sys, os
import errno, pathlib, re
import datetime, time
import json, requests
import sqlite3

### Variables that need to be set by user
urlscan_api = ''
### urlscan's config directory
urlscan_dir = str(pathlib.Path.home()) + '/.urlscan'

### urlscan's local database
urlscan_default_db = urlscan_dir + '/urlscan.db'


### Stop editing!

if not os.path.exists(urlscan_dir):
        os.makedirs(urlscan_dir)

## argparse arguments
parser = argparse.ArgumentParser(description="Wrapper for urlscan.io's API")

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

## Scan parser
parser_scan = subparsers.add_parser('scan', help='scan a url')
parser_scan.add_argument('--url', help='URL(s) to scan', nargs='+', metavar='URL', required='True')
parser_scan.add_argument('--db', help='specify different database file initiated scans will be saved to', metavar='FILE', default=urlscan_default_db)
parser_scan.add_argument('-f', '--file', help='file with url(s) to scan')
parser_scan.add_argument('-q', '--quiet', help='suppress output', action="store_true")

## Search parser
parser_search = subparsers.add_parser('search', help='search database for UUID of url')
parser_search.add_argument('--host', help='host(s) to search for matching UUID', nargs='+', metavar='HOST')
parser_search.add_argument('--db', help='specify different database file to search', metavar='FILE', default=urlscan_default_db)

## Retrieve parser
parser_retrieve = subparsers.add_parser('retrieve', help='retrieve scan results')
parser_retrieve.add_argument('--uuid', help='UUID(s) to retrieve scans for', nargs='+', metavar='UUID', required='True')
parser_retrieve.add_argument('-d', '--dir', help='directory to save scans to', metavar='DIRECTORY', default='saved_scans')
parser_retrieve.add_argument('-q', '--quiet', help='suppress output', action="store_true")

args = parser.parse_args()


if urlscan_api == '':
    print('Please input valid urlscan_api value in ' + sys.argv[0])
    sys.exit(1)


def submit():
    if args.file: 
        urls_to_scan = [line.rstrip('\n') for line in open(args.file)]
    else:
        urls_to_scan = args.url

    for target_urls in urls_to_scan:
        headers = {
            'Content-Type': 'application/json',
            'API-Key': urlscan_api,
        }

        data = '{"url": "%s"}' % target_urls

        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=data)

        ## end POST request

        r = response.content.decode("utf-8")

        if not args.quiet:
            print(r)

        if args.db:
            save_history(target_urls, r)


        time.sleep(3)


def search():
    search_urls = args.host
    db_connect()
    for url in search_urls:
        t = (url,)
        c.execute('SELECT * FROM scanned_urls WHERE url=?', t)
        print(c.fetchone())
    

def query():
    for target_uuid in args.uuid:
        response = requests.get("https://urlscan.io/api/v1/result/%s" % target_uuid)

        r = response.content.decode("utf-8")

        if not args.quiet:
            print(r)

        if hasattr(args, 'dir'):
            save_to_dir(str(args.dir), target_uuid, str(r))

        time.sleep(3)


def save_history(x, y):
    ### extract UUID from json
    matched_lines = [line for line in y.split('\n') if "uuid" in line]
    result = ''.join(matched_lines)
    result = result.split(":",1)[1]
    uuid = re.sub(r'[^a-zA-Z0-9=-]', '', result)
    ### end UUID extraction

    target_url = str(x)
    current_time = int(time.time())
    human_readable_time = str(datetime.datetime.fromtimestamp(current_time))
    db_connect()
    c.execute('''CREATE TABLE IF NOT EXISTS scanned_urls (url, uuid, datetime TEXT PRIMARY KEY)''')
    c.execute("INSERT OR REPLACE INTO scanned_urls VALUES (?, ?, ?)", (target_url, uuid, human_readable_time))
    conn.commit()
    conn.close()


def save_to_dir(x, y, z):
    if not os.path.exists(x):
        os.makedirs(x)

    save_file_name = x + '/' + y

    path_to_file = pathlib.Path(save_file_name)
    if not path_to_file.is_file():
        with open(save_file_name, 'a') as out:
            out.write(z)

def db_connect():
    global conn
    conn = sqlite3.connect(args.db)
    global c
    c = conn.cursor()


def main():
    if hasattr(args, 'url'):
        submit()

    if hasattr(args, 'host'):
        search()

    if hasattr(args, 'uuid'):
        query()


if __name__ == '__main__':
    main()
