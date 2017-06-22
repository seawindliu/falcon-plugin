Nginx performance monitor plugin for Open-Falcon 
--------------------------------

监控数据采集原理
---------------
1 通过nginx配置的nginx_status获取nginx信息

2 获取的nginx status信息通过open-falcon agent api

3 通过cron每分钟采集上报

环境要求
---------------
操作系统: Linux

Python 2.6

PyYAML > 3.10

python-requests > 0.11

nginx部署
-------------------
1 nginx.conf必须配置
  server {
       listen       88 ;

       location /nginx_status {
          stub_status on;
          access_log off;
          allow 127.0.0.1;
          deny all;
       }
    }
1 目录解压到/opt/program/falcon/plugin/nginx
3 配置当前服务器: 
open_falcon_api: 'http://127.0.0.1:1988/v1/push'
status_url: 'http://127.0.0.1:88/nginx_status'
endpoint: 'fuzhou28'
4 配置crontab, 修改/opt/program/falcon/plugin/nginx/nginx_monitor_cron文件中的安装path; cp nginx_monitor_cron /etc/cron.d/ 
5 几分钟后，可从open-falcon的dashboard中查看Nginx metric
6 endpoint默认是hostname

Nginx falcon screen
----------

采集的Nginx指标
--------------------------------
| Counters | Type | Notes|
|-----|------|------|
|active_connections|         GAUGE   |活跃的连接数           
|accepts|                    GAUGE   |接收的连接数                                            
|handled|                    GAUGE   |创建的连接数                               
|requests|                   GAUGE   |处理的连接数                                            
|reading|                    GAUGE   |读取客户端的连接数                                      
|writing|                    GAUGE   |响应数据到客户端的连接数                                    
|waiting|                    GAUGE   |开启 keep-alive 的情况下,这个值等于 active – (reading+writing), 意思就是 Nginx 已经处理完正在等候下一次请求指令的驻留连接.                                    



建议设置监控告警项
-----------------------------
说明:系统级监控项由falcon agent提供；监控触发条件根据场景自行调整
--------------------------------

|告警项|
|-----|
|load.1min>10|
|cpu.idle<10|
|df.bytes.free.percent<30|
|df.bytes.free.percent<10|
|mem.memfree.percent<20|
|mem.memfree.percent<10|
|mem.memfree.percent<5|
|mem.swapfree.percent<50|
|mem.memused.percent>=50|
|mem.memused.percent>=10|
|net.if.out.bytes>94371840|
|net.if.in.bytes>94371840|
|disk.io.util>90|
|mongo_local_alive=0|
|page_faults>100|
|connections_current>5000|
|connections_used_percent>60|
|connections_used_percent>80|
|connections_totalCreated>1000|
|globalLock_currentQueue_total>10|
|globalLock_currentQueue_readers>10|
|globalLock_currentQueue_writers>10|
|opcounters_command|
|opcounters_insert|
|opcounters_delete|
|opcounters_update|
|opcounters_query|
|opcounters_getmore|
|opcountersRepl_command|
|opcountersRepl_insert|
|opcountersRepl_delete|
|opcountersRepl_update|
|opcountersRepl_query|
|opcountersRepl_getmore|
|network_bytesIn|
|network_bytesOut|
|network_numRequests|
|repl_health=0|
|repl_myState not 1/2/7|
|repl_oplog_window<168|
|repl_oplog_window<48|
|replication_lag_percent>50|
|repl_lag>60|
|repl_lag>300|
|shards_mongosSize
