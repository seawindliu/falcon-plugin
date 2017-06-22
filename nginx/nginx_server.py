#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'liuxl'

import re
import urllib2

class NginxStats:

    def __init__(self, url=''):
        self._url = url

    def stats(self):
        c = urllib2.urlopen(self._url, None, 2)
        data = c.read()
        c.close()

        matchActive = re.search(r'Active connections:\s+(\d+)', data)
        matchHistory = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)', data)
        matchCurrent = re.search(r'Reading:\s*(\d+)\s*Writing:\s*(\d+)\s*'
            'Waiting:\s*(\d+)', data)

        if not matchActive or not matchHistory or not matchCurrent:
            raise Exception('Unable to parse {0}' . format(url))

        result = {}
        result['active_connections'] = int(matchActive.group(1))
        result['accepts'] = int(matchHistory.group(1))
        result['handled'] = int(matchHistory.group(2))
        result['requests'] = int(matchHistory.group(3))
        result['reading'] = int(matchCurrent.group(1))
        result['writing'] = int(matchCurrent.group(2))
        result['waiting'] = int(matchCurrent.group(3))

        return result