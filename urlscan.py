#!/usr/bin/env python3
import argparse
import sys, os
import errno, pathlib, re
import datetime, time
import json, requests, urllib.request
import sqlite3

### Variables that need to be set by user

### urlscan's config directory
urlscan_dir = str(pathlib.Path.home()) + '/.urlscan'

saved_scan_dir = urlscan_dir + '/saved_scans'

### urlscan's local database
urlscan_default_db = urlscan_dir + '/urlscan.db'


### Stop editing!

if not os.path.exists(urlscan_dir):
        os.makedirs(urlscan_dir)

## argparse arguments
parser = argparse.ArgumentParser(description="Wrapper for urlscan.io's API")

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

## Init subparser
parser_init = subparsers.add_parser('init', help='initialize urlscan-py with API key')
parser_init.add_argument('--api_key', help='urlscan API key', metavar='KEY')
parser_init.add_argument('--db', help='specify different database file to search', metavar='FILE', default=urlscan_default_db)

## Scan parser
parser_scan = subparsers.add_parser('scan', help='scan a url')
parser_scan.add_argument('--url', help='URL(s) to scan', nargs='+', metavar='URL')
parser_scan.add_argument('--db', help='specify different database file initiated scans will be saved to', metavar='FILE', default=urlscan_default_db)
parser_scan.add_argument('-f', '--file', help='file with url(s) to scan')
parser_scan.add_argument('-q', '--quiet', help='suppress output', action="store_true")
parser_scan.add_argument('--api', help='urlscan API key', metavar='KEY')

## Search parser
parser_search = subparsers.add_parser('search', help='search database for UUID of url')
parser_search.add_argument('--host', help='host(s) to search for matching UUID', nargs='+', metavar='HOST')
parser_search.add_argument('--db', help='specify different database file to search', metavar='FILE', default=urlscan_default_db)
parser_search.add_argument('--api', help='urlscan API key', metavar='KEY')

## Retrieve parser
parser_retrieve = subparsers.add_parser('retrieve', help='retrieve scan results')
parser_retrieve.add_argument('--uuid', help='UUID(s) to retrieve scans for', nargs='+', metavar='UUID', required='True')
parser_retrieve.add_argument('--db', help='specify different database file to query', metavar='FILE', default=urlscan_default_db)
parser_retrieve.add_argument('--api', help='urlscan API key', metavar='KEY')
parser_retrieve.add_argument('-d', '--dir', help='directory to save scans to', metavar='DIRECTORY', default=saved_scan_dir)
parser_retrieve.add_argument('-q', '--quiet', help='suppress output', action="store_true")
parser_retrieve.add_argument('--dom', help='urlscan retrieve DOM', action="store_true")
parser_retrieve.add_argument('--png', help='urlscan retrieve screenshot', action="store_true")

args = parser.parse_args()


def connect_db():
    global conn
    conn = sqlite3.connect(args.db)
    global c
    c = conn.cursor()


def add_key_value():
    connect_db()
    global urlscan_api
    try:
        c.execute('''CREATE TABLE api (key TEXT PRIMARY KEY)''')
    except sqlite3.OperationalError:
        pass
    if hasattr(args, 'api_key'):
        urlscan_api = args.api_key
    else:
        urlscan_api = input('Please enter API key: ')
    c.execute("INSERT OR REPLACE INTO api VALUES (?)", (urlscan_api,))
    conn.commit()
    sys.exit(0)


def get_key_value():
    connect_db()
    global urlscan_api
    try:
        c.execute("SELECT * FROM api")
    except sqlite3.OperationalError:
        add_key_value()
    db_extract = c.fetchone()
    try:
        urlscan_api = ''.join(db_extract)
    except TypeError:
        print('Invalid API entry in database.')
        sys.exit(1)

def initialize():
    global urlscan_api
    if hasattr(args, 'api_key'):
        try:
            get_key_value()
            overwrite = input('API already exists in database. Overwrite? (y/n)')
            if overwrite == 'y':
                add_key_value()
        except sqlite3.OperationalError:
            add_key_value()
        sys.exit(0)
    if args.api:
        urlscan_api = args.api
    else:
        get_key_value()


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
    connect_db()
    for url in search_urls:
        t = (url,)
        c.execute('SELECT * FROM scanned_urls WHERE url=?', t)
        print(c.fetchone())
    

def download_dom(x, y):
    target_uuid = x
    dom_url = 'https://urlscan.io/dom/' + target_uuid + '/'
    target_dom = y + 'site.dom'
    try:
        os.makedirs(y)
    except FileExistsError:
        pass
    try:
        urllib.request.urlretrieve(dom_url, str(target_dom))
    except FileExistsError:
        pass
    

def download_png(x, y):
    target_uuid = x
    png_url = 'https://urlscan.io/screenshots/' + target_uuid + '.png'
    target_png = y + 'screenshot.png'
    try:
        os.makedirs(y)
    except FileExistsError:
        pass
    try:
        urllib.request.urlretrieve(png_url, str(target_png))
    except FileExistsError:
        pass



def query():
    for target_uuid in args.uuid:
        response = requests.get("https://urlscan.io/api/v1/result/%s" % target_uuid)

        formatted_uuid = target_uuid.replace("-", "_")
        target_dir = args.dir + '/' + formatted_uuid + '/'
        
        r = response.content.decode("utf-8")

        if not args.quiet:
            print(r)

        if hasattr(args, 'dir'):
            save_to_dir(target_dir, target_uuid, str(r))
        
        if hasattr(args, 'dom'):
            download_dom(target_uuid, target_dir)

        if hasattr(args, 'png'):
            download_png(target_uuid, target_dir)

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
    connect_db()
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

    

def main():
    initialize()
    if hasattr(args, 'url'):
        submit()

    if hasattr(args, 'host'):
        search()

    if hasattr(args, 'uuid'):
        query()


if __name__ == '__main__':
    main()
