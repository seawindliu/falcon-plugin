#!/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'liuxl'

import json
import time
import socket
import os
import re
import sys
import yaml
import commands
import requests

class RedisStats:
    # 如果你是自己编译部署到redis，请将下面的值替换为你到redis-cli路径
    _redis_cli = '/usr/bin/redis-cli'
    _stat_regex = re.compile(ur'(\w+):([0-9]+\.?[0-9]*)\r')

    def __init__(self,  port='6379', passwd=None, host='127.0.0.1'):
        self._cmd = '%s -h %s -p %s info' % (self._redis_cli, host, port)
        if passwd not in ['', None]:
            self._cmd = '%s -h %s -p %s -a %s info' % (self._redis_cli, host, port, passwd)

    def stats(self):
        ' Return a dict containing redis stats '
        info = commands.getoutput(self._cmd)
        return dict(self._stat_regex.findall(info))


def main():
    #ip = socket.gethostname()
    open_falcon_api = 'http://127.0.0.1:1988/v1/push'
    #ip = socket.gethostname()
    fconf = open("redis.conf")
    y = yaml.load(fconf)
    fconf.close()
    insts_list = y["items"]
    timestamp = int(time.time())
    step = 60
    
    monit_keys = [
        ('connected_clients','GAUGE'), 
        ('blocked_clients','GAUGE'), 
        ('used_memory','GAUGE'),
        ('used_memory_rss','GAUGE'),
        ('mem_fragmentation_ratio','GAUGE'),
        ('total_commands_processed','COUNTER'),
        ('rejected_connections','COUNTER'),
        ('expired_keys','COUNTER'),
        ('evicted_keys','COUNTER'),
        ('keyspace_hits','COUNTER'),
        ('keyspace_misses','COUNTER'),
        ('keyspace_hit_ratio','GAUGE'),
    ]
    for inst in insts_list:
        p = []
        endpoint = socket.gethostname()
        if inst.has_key('endpoint') == True and inst["endpoint"]!="":
            endpoint = inst["endpoint"]
        host = inst["host"]
        port = inst["port"]
        passwd = inst["passwd"]
        metric = "redis"
        tags = 'port=%s' % port

        try:
            conn = RedisStats(port, passwd,host)
            stats = conn.stats()
        except Exception,e:
            continue

        for key,vtype in monit_keys:
            #一些老版本的redis中info输出的信息很少，如果缺少一些我们需要采集的key就跳过
            if key not in stats.keys():
                continue
            #计算命中率
            if key == 'keyspace_hit_ratio':
                try:
                    value = float(stats['keyspace_hits'])/(int(stats['keyspace_hits']) + int(stats['keyspace_misses']))
                except ZeroDivisionError:
                    value = 0
            #碎片率是浮点数
            elif key == 'mem_fragmentation_ratio':
                value = float(stats[key])
            else:
                #其他的都采集成counter，int
                try:
                    value = int(stats[key])
                except:
                    continue
            
            i = {
                'Metric': '%s.%s' % (metric, key),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': step,
                'Value': value,
                'CounterType': vtype,
                'TAGS': tags
            }
            p.append(i)

    #print json.dumps(p, sort_keys=True,indent=4)
    r = requests.post(open_falcon_api, data=json.dumps(p))
    print r.text

if __name__ == '__main__':
    main()

