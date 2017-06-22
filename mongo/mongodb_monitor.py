#! /bin/env python
#-*- coding:utf8 -*-

import sys
import os
import time
import datetime
import socket
import yaml
import requests
import json

from mongodb_server import mongodbMonitor

falcon_client = "http://127.0.0.1:1988/v1/push"
ts = int(time.time())
# all falcon counter type metrics list
mongodb_counter_metric = [
    "asserts_msg",
    "asserts_regular",
    "asserts_rollovers",
    "asserts_user",
    "asserts_warning",
    "page_faults",
    "connections_totalCreated",
    "locks_Global_acquireCount_ISlock",
    "locks_Global_acquireCount_IXlock",
    "locks_Global_acquireCount_Slock",
    "locks_Global_acquireCount_Xlock",
    "locks_Global_acquireWaitCount_ISlock",
    "locks_Global_acquireWaitCount_IXlock",
    "locks_Global_timeAcquiringMicros_ISlock",
    "locks_Global_timeAcquiringMicros_IXlock",
    "locks_Database_acquireCount_ISlock",
    "locks_Database_acquireCount_IXlock",
    "locks_Database_acquireCount_Slock",
    "locks_Database_acquireCount_Xlock",
    "locks_Collection_acquireCount_ISlock",
    "locks_Collection_acquireCount_IXlock",
    "locks_Collection_acquireCount_Xlock",
    "opcounters_command",
    "opcounters_insert",
    "opcounters_delete",
    "opcounters_update",
    "opcounters_query",
    "opcounters_getmore",
    "opcountersRepl_command",
    "opcountersRepl_insert",
    "opcountersRepl_delete",
    "opcountersRepl_update",
    "opcountersRepl_query",
    "opcountersRepl_getmore",
    "network_bytesIn",
    "network_bytesOut",
    "network_numRequests",
    "backgroundFlushing_flushes",
    "backgroundFlushing_last_ms",
    "cursor_timedOut",
    "wt_cache_readinto_bytes",
    "wt_cache_writtenfrom_bytes",
    "wt_bm_bytes_read",
    "wt_bm_bytes_written",
    "wt_bm_blocks_read",
    "wt_bm_blocks_written"
]

fconf = open("mongo.conf")
y = yaml.load(fconf)
fconf.close()
items = y["items"]
for inst in items:
    endpoint = socket.gethostname()
    if inst.has_key('endpoint') == True and inst["endpoint"]!="":
            endpoint = inst["endpoint"]
    tag = "mongo=" + str(inst["port"])
    metric = "mongo"
    
    data = []
    monitor = mongodbMonitor()
    err,conn = monitor.mongodb_connect(host=inst["host"],port=inst["port"], user=inst["user"], password=inst["password"]) 
    if err != 0:
        key_item_dict = {"endpoint": endpoint, "metric": '%s.%s' % (metric, "mongo_is_alive"), "tags":tag , "timestamp":ts, "value": 0, "step": 60, "counterType": "GAUGE"}
        data.append(key_item_dict)
        r = requests.post(falcon_client,json.dumps(data))
        continue   #The instance is dead. upload the "mongo_is_local=0" key, then continue.

    key_item_dict = {"endpoint": endpoint, "metric": '%s.%s' % (metric, "mongo_is_alive"), "tags":tag , "timestamp":ts, "value": 1, "step": 60, "counterType": "GAUGE"}
    data.append(key_item_dict)  
    mongodb_dict = monitor.get_mongo_monitor_data(conn)
    mongodb_dict_keys = mongodb_dict.keys()
    for mongodb_metric in mongodb_dict_keys:
        if mongodb_metric in mongodb_counter_metric :
            key_item_dict = {"endpoint": endpoint, "metric": '%s.%s' % (metric, mongodb_metric), "tags":tag , "timestamp":ts, "value": mongodb_dict[mongodb_metric], "step": 60, "counterType": "COUNTER"}
        else:
            key_item_dict =  {"endpoint": endpoint, "metric": '%s.%s' % (metric, mongodb_metric), "tags":tag , "timestamp":ts, "value": mongodb_dict[mongodb_metric], "step": 60, "counterType": "GAUGE"}
        data.append(key_item_dict)
#print json.dumps(data,sort_keys=True,indent=4)        
r = requests.post(falcon_client,json.dumps(data))
print r.text
