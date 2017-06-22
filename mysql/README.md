open-falcon mysql监控脚本
环境准备:
pip install MySQL-python
================================================================
指标说明：收集指标里的COUNTER表示每秒执行次数，GAUGE表示直接输出值。

 指标	类型	说明
 Undo_Log_Length	 GAUGE	未清除的Undo事务数
 Com_select	 COUNTER	 select/秒=QPS
 Com_insert	 COUNTER	 insert/秒
 Com_update	 COUNTER	 update/秒
 Com_delete	 COUNTER	 delete/秒
 Com_replace	 COUNTER	 replace/秒
 MySQL_QPS	 COUNTER	 QPS
 MySQL_TPS	 COUNTER	 TPS 
 ReadWrite_ratio	 GAUGE	 读写比例
 Innodb_buffer_pool_read_requests	 COUNTER	 innodb buffer pool 读次数/秒
 Innodb_buffer_pool_reads	 COUNTER	 Disk 读次数/秒
 Innodb_buffer_read_hit_ratio	 GAUGE	 innodb buffer pool 命中率
 Innodb_buffer_pool_pages_flushed	 COUNTER	 innodb buffer pool 刷写到磁盘的页数/秒
 Innodb_buffer_pool_pages_free	 GAUGE	 innodb buffer pool 空闲页的数量
 Innodb_buffer_pool_pages_dirty	 GAUGE	 innodb buffer pool 脏页的数量
 Innodb_buffer_pool_pages_data	 GAUGE	 innodb buffer pool 数据页的数量
 Bytes_received	 COUNTER	 接收字节数/秒
 Bytes_sent	 COUNTER	 发送字节数/秒
 Innodb_rows_deleted	 COUNTER	 innodb表删除的行数/秒
 Innodb_rows_inserted	 COUNTER 	 innodb表插入的行数/秒
 Innodb_rows_read	 COUNTER 	 innodb表读取的行数/秒
 Innodb_rows_updated 	 COUNTER 	 innodb表更新的行数/秒
 Innodb_os_log_fsyncs	 COUNTER 	 Redo Log fsync次数/秒 
 Innodb_os_log_written	 COUNTER 	 Redo Log 写入的字节数/秒
 Created_tmp_disk_tables	 COUNTER 	 创建磁盘临时表的数量/秒
 Created_tmp_tables	 COUNTER 	 创建内存临时表的数量/秒
 Connections	 COUNTER 	 连接数/秒
 Innodb_log_waits	 COUNTER 	 innodb log buffer不足等待的数量/秒
 Slow_queries	 COUNTER 	 慢查询数/秒
 Binlog_cache_disk_use	 COUNTER 	 Binlog Cache不足的数量/秒

================================
使用说明：读取配置到都数据库列表执行，配置文件格式如下(mysql.conf)：

IP,Port,User,Password,endpoint

192.168.2.21,3306,root,123,mysql-21:3306
192.168.2.88,3306,root,123,mysql-88:3306
最后执行：

python mysql_monitor.py mysql.conf


