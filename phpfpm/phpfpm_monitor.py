#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuxl'

import requests
import json
import time
import socket
import yaml
import urllib
import urllib2

class PhpfpmStats:
    def __init__(self,listen_addr,status_path,status_url):
        self.listen_addr     = listen_addr
        self.status_path     = status_path
        self.status_url      = status_url
    
    def stats(self):
        try:
            data = urllib2.urlopen(self.status_url ).read()
            status = json.loads(data)  
            return status
        except urllib2.HTTPError as err:
            print str(err)
            status = {}
            return status   

def main():
    open_falcon_api = 'http://127.0.0.1:1988/v1/push'
    #ip = socket.gethostname()
    fconf = open("phpfpm.conf")
    y = yaml.load(fconf)
    fconf.close()
    insts_list = y["items"]
    timestamp = int(time.time())
    step = 60
    for inst in insts_list:
        endpoint = socket.gethostname()
        if inst.has_key('endpoint') == True and inst["endpoint"]!="":
            endpoint = inst["endpoint"]
        listen_addr = inst["listen_addr"]
        status_path = inst["status_path"]
        status_url  = inst["status_url"]
        metric = "phpfpm"
        timestamp = int(time.time())
        step      = 60
        tags = ''

        monitor_keys = [
            # 'pool
            # 'start_time'
            # 'process_manager'
            # 'start_since'
            ('active_processes', 'GAUGE'),
            ('accepted_conn', 'COUNTER'),
            ('listen_queue', 'GAUGE'),
            ('idle_processes', 'GAUGE'),
            ('slow_requests', 'GAUGE'),
            ('max_active_processes', 'GAUGE'),
            ('max_children_reached', 'GAUGE'),
            ('max_listen_queue', 'GAUGE'),
            ('total_processes', 'GAUGE'),
            ('listen_queue_len', 'GAUGE'),
        ]
        try:
            conn = PhpfpmStats(listen_addr,status_path,status_url)
            status = conn.stats()
        except:
            continue 
        tags = 'pool=%s' % status['pool']
        data = []
        for key, vtype in monitor_keys:
            value = int(status[key.replace('_', ' ')])
            i = {
                'Metric': '%s.%s' % (metric, key),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': step,
                'Value': value,
                'CounterType': vtype,
                'TAGS': tags
            }
            data.append(i)

        #print json.dumps(data,sort_keys=True,indent=4)
        r = requests.post(open_falcon_api, data=json.dumps(data))
        print r.text

if __name__ == '__main__':
    main()
