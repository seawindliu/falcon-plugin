#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'liuxl'

import requests
import json
import time
import socket
import yaml

from nginx_server import NginxStats

fconf = open("nginx.conf")
y = yaml.load(fconf)
fconf.close()

endpoint = socket.gethostname()
if y.has_key('endpoint') == True:
    endpoint = str(y["endpoint"])

metric = 'nginx'
open_falcon_api = y["open_falcon_api"]
timestamp = int(time.time())
step = 60
tags = ''

conn = NginxStats(url=str(y["status_url"]))
stats = conn.stats()

data = []
for key in stats:
    i = {
        'metric': '%s.%s' % (metric, key),
        'endpoint': endpoint,
        'timestamp': timestamp,
        'step': step,
        'value': stats[key],
        'counterType': 'GAUGE',
        'tags': tags
    }
    data.append(i)

#print json.dumps(data,sort_keys=True,indent=4)
r = requests.post(open_falcon_api, data=json.dumps(data))
print r.text