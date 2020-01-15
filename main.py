#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from collect import collect
import argparse
import logging

parser = argparse.ArgumentParser('')
parser.add_argument('filename', type=str, help='Filename')
parser.add_argument('--directory', '-D', type=Path, dest='directory', action='store', default=Path.cwd(), help='File directory')
parser.add_argument('--number-of-pages', '-n', type=int, dest='number', action='store', default=10,
    help='Number of displayed requested pages that don\'t exist')

ARGS = parser.parse_args()

filepath = (ARGS.directory / ARGS.filename).absolute()

# Collecting data from the log
data, pages = collect(filepath)

# Adress with the highest number of requests
requests = []
for ip_addr, d in data.items():
    x = (d['requests'], ip_addr)
    requests.append(x)
requests.sort(reverse=True)
print(f'The highest number of requests were from the adress {requests[0][1]}')

# Adress that requested the largest amount of data
req_bytes = [(v['bytes'], ip) for ip, v in data.items()] # list comprehension
req_bytes.sort(reverse=True)
print(f'The largest number of bytes was sent to the adress {req_bytes[0][1]}')

# Adress with the largest number of requests per unit of time
density = [
    (
        v['requests'] / (v['last_ts'] - v['first_ts']).total_seconds(),
        ip
    )
    for ip, v in data.items()
]
density.sort(reverse=True)
print(f'The highest density of request was from the adress {density[0][1]}')

# The most requested page
page_requests = [(v['requests'], p) for p, v in pages.items()]
page_requests.sort(reverse=True)
print(f'The most requested page: {page_requests[0][1]}')

# The page that haven't been requested longer than any, but still exist
unrequested_pages=[]
for page, v in pages.items():
    if v['response_code'] == '200':
        x = (v['last_ts'], page)
        unrequested_pages.append(x)
unrequested_pages.sort()
print(f'The page {unrequested_pages[0][1]} haven\'t been requested longer than any')

# The pages that were requested but don't exist
print(f'List of the first {ARGS.number} pages that have been requested but don\'t exist:')
absent_pages = [ (p, v['response_code']) for p, v in pages.items()]
absent_pages.sort()
for i in range(ARGS.number):
    if absent_pages[i][1] == '404':
        print(absent_pages[i][0])

# TODO:
# Application log
