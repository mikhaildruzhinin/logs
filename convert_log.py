#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

DATE = re.compile(r'''
    \[\s*
    (\d\d)      # day
    \s*/\s*
    (\S\S\S?)   #  month
    \s*/\s*
    (\d\d\d\d)  # year
    \s*:\s*
    (\d\d)      # hour
    \s*:\s*
    (\d\d)      # minute
    \s*:\s*
    (\d\d)      # second
    \s*\]
    ''', re.VERBOSE)

ADRESS = re.compile(r'''
    "GET
    \s*
    (\S+)       # adress
    \s*
    HTTP/1\.[01]
    ''', re.VERBOSE) 

def custom(text):
    '''
    Converting a log line to a more convenient form
    '''
    x = text.split()
    
    # IP adress
    ip_addr = x[0]
    
    # Response code
    response_code = x[-2]
    
    # Response in bytes
    if response_code == '200':
        response_size = int(x[-1])
    else:
        response_size = None
    
    # Request timestamp
    timestamp = None
    m = DATE.search(text)
    if m: # if m := DATE.search(text) Python 3.8 
        d, m, y, hr, mn, sc = map(int, m.groups())
        timestamp = datetime(y, m, d, hr, mn, sc)
    page = None
    m = ADRESS.search(text)
    if m:
        page = m.group(1)
    
    return {
        'ip_addr':ip_addr,
        'response_code':response_code,
        'response_size':response_size,
        'timestamp':timestamp,
        'page':page,
    }
