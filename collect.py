#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from convert_log import custom

# Collecting data from the log
def collect(filepath):
    data = {}
    pages = {}
    with open(filepath, 'rt', encoding='utf-8') as src:
        for x in map(custom, src):
            if x['ip_addr'] not in data:
                d = {
                    'requests': 0,
                    'bytes':0,
                    'first_ts':x['timestamp'],
                    'last_ts':x['timestamp'],
                }
                data[x['ip_addr']] = d
            else:
                d = data[x['ip_addr']]
            d['requests'] += 1
            #d['bytes'] += x['response_size'] # can't add int and None
            try:
                d['bytes'] += x['response_size']
            except TypeError:
                pass # exception supress
            if d['first_ts'] > x['timestamp']:
                d['first_ts'] = x['timestamp']
            d['last_ts'] = max(d['last_ts'], x['timestamp'])
            if x['page'] not in pages:
                d = {
                    'response_code':x['response_code'],
                    'requests':0,
                    #'first_ts':x['timestamp'],
                    'last_ts':x['timestamp'],
                }
                pages[x['page']] = d
            else:
                d = pages[x['page']]
            d['requests'] += 1
            #d['first_ts'] = min(d['first_ts'], x['timestamp'])
            d['last_ts'] = max(d['last_ts'], x['timestamp'])
    return data, pages # returns a tuple of dicts
