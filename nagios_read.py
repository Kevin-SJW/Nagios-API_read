#coding:utf-8
import datetime
import os
import requests
import time
import json
from nagiossql import *
import pika
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
# import sys
# sys.setrecursionlimit(1000000)
#引入shell交互
shell_command='nohup /var/www/html/nagios-api-1.2.2/nagios-api -p 6060 -c /usr/local/nagios/var/rw/nagios.cmd -s /usr/local/nagios/var/status.dat -l /usr/local/nagios/var/nagios.log &'
os.system(shell_command)
time.sleep(1)
rabbitmqhost='192.168.1.133'
queuesql='nagios'
numbermsg=1
conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmqhost))
channel = conn.channel()
# hostname='192.168.1.133'
# conn = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
# channel = conn.channel()
# msg = {}
url='http://192.168.1.135:6060/state'
nodeserver = '192.168.1.136'
output='plugin_output'
state='current_state'
monitored_host = 'localhost'
NagiosServer = 'Nagios-Server'
MapMonitor = 'map-PC'
nagiosstate={'0':'ok','1':'warning','2':'critical','3':'unknown'}

def getnagios():
    r=requests.get(url)
    return r.json()

def time_convert(last_check_input):
    # str to date
    # 字符串转化为日期
    timeStamp = last_check_input + 28800
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    last_check = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return last_check

def NagiosInsert():
    for key1, value1 in initmsg.items():
        if key1 == 'admin-PC':
            continue


        if key1 == NagiosServer:
            # continue
            print value1['services']
            for key2, value2 in value1['services'].items():
                print key2
                print value2
                if key2 in ['Current Load', 'Current Users', 'HTTP', 'PING',
                                'Root Partition', 'SSH', 'Swap Usage', 'Total Processes']:
                        # continue
                    nagios_monitor = NagiosMonitor()
                    nagios_monitor.sys_time = time_convert(time.time())
                    nagios_monitor.hostname = key1
                    nagios_monitor.services = key2
                    nagios_monitor.state = nagiosstate[value2['current_state']]
                    # print nagiosstate[value2['current_state']]
                    nagios_monitor.current_attempt = value2['current_attempt']
                    nagios_monitor.last_check = time_convert(float(value2['last_check']))
                    nagios_monitor.last_state_change = time_convert(float(value2['last_state_change']))
                    nagios_monitor.output = value2[output]
                    session.add(nagios_monitor)
                    # session.flush()
                    session.commit()


        if key1 == monitored_host:
            # continue
            print value1['services']
            for key2, value2 in value1['services'].items():
                print key2
                print value2
                if key2 in ['Check DatabaseClean','Check Zombie Procs', 'Check fusion', 'Check geofence', 'Check r_udp.py',
                            'Check r_ais','Check r_dian','Check playback','Check pack_sys','Check trackAnalysisServer',
                            'Check Disk sda1','Check rabbit Procs', 'Current Load', 'Current Users', 'check-host-alive']:
                     # continue
                    nagios_monitor = NagiosMonitor()
                    nagios_monitor.sys_time = time_convert(time.time())
                    nagios_monitor.hostname = key1
                    nagios_monitor.services = key2
                    nagios_monitor.state = nagiosstate[value2['current_state']]
                    # print nagiosstate[value2['current_state']]
                    nagios_monitor.current_attempt = value2['current_attempt']
                    nagios_monitor.last_check = time_convert(float(value2['last_check']))
                    nagios_monitor.last_state_change = time_convert(float(value2['last_state_change']))
                    nagios_monitor.output = value2[output]
                    session.add(nagios_monitor)
                    # session.flush()
                    session.commit()


        if key1 == MapMonitor:
            # continue
            print value1['services']
            for key2, value2 in value1['services'].items():
                print key2
                print value2
                if key2 in ['ArcGIS License Manager', 'ArcGIS Server', 'C:\ Drive Space', 'CPU Load',
                                    'Explorer', 'Memory Usage', 'NSClient++ Version', 'Uptime', 'W3SVC']:
                    nagios_monitor = NagiosMonitor()
                    nagios_monitor.sys_time = time_convert(time.time())
                    nagios_monitor.hostname = key1
                    nagios_monitor.services = key2
                    nagios_monitor.state = nagiosstate[value2['current_state']]
                    # print nagiosstate[value2['current_state']]
                    nagios_monitor.current_attempt = value2['current_attempt']
                    nagios_monitor.last_check = time_convert(float(value2['last_check']))
                    nagios_monitor.last_state_change = time_convert(float(value2['last_state_change']))
                    nagios_monitor.output = value2[output]
                    session.add(nagios_monitor)
                    # session.flush()
                    session.commit()

# 字典比较找差别，并发送消息队列，插入数据库
def cmp_diff(src_data,dst_data):
    zip(src_data,dst_data)
    list(zip(src_data,dst_data))
    for (key,src_data[key]),(key, dst_data[key]) in zip(src_data.items(),dst_data.items()):
        # for (key, dst_data[key]) in zip(src_data, dst_data):
            # for (key,dst_data[key]) in dst_data.items():
        global initmsg
        # print str(key)
        # print src_data[key]
        # print dst_data[key]
        if isinstance(src_data, dict) and isinstance(dst_data, dict):
            """若为dict格式"""
            for key in dst_data.keys():
                if key not in src_data.keys():
                    print("src不存在这个key")
                else:
                    if src_data[key] == dst_data[key]:
                        print "nagios监控信息无变化"
                    else:
                        print "nagios监控信息有变化"
                        src_data[key] = dst_data[key]
                        json_str2 = json.dumps(src_data)
                        body2 = json_str2
                        channel.basic_publish(exchange='',
                                                  routing_key='nagios_alert',
                                                  body=body2)

                        print"变化信息插入数据库"
                        initmsg = getnagios()['content']
                        # 消除乱码

                        initmsg = eval(str(initmsg).replace('\u2013', ''))
                        NagiosInsert()
                            # session.add(nagios_monitor)
                            # # session.flush()
                            # session.commit()


initmsg = getnagios()['content']
    #消除乱码

initmsg=eval(str(initmsg).replace('\u2013',''))
NagiosInsert()

def getinitmsg(initmsg):
    initmsg = getnagios()['content']
    # 消除乱码
    initmsg = eval(str(initmsg).replace('\u2013', ''))

    for key1, value1 in initmsg.items():
        if key1 == 'admin-PC':
            continue


        if key1 == monitored_host:
            # continue
            print value1['services']
            for key2, value2 in value1['services'].items():
                print key2
                print value2
                if key2 in ['Check DatabaseClean','Check Zombie Procs', 'Check fusion', 'Check geofence', 'Check r_udp.py',
                            'Check r_ais','Check r_dian','Check playback','Check pack_sys','Check trackAnalysisServer',
                            'Check Disk sda1','Check rabbit Procs', 'Current Load', 'check-host-alive']:
                     # continue

                    hostname = key1
                    print hostname
                    services = key2
                    print services
                    state = nagiosstate[value2['current_state']]
                    print state

                    PathData = {
                         'hostname': str(hostname),
                         'services': str(services),
                         'state': str(state),
                    }
                     # 将相关状态信息以字典的形式存储
                    json_str1 = json.dumps(PathData)
                    body1 = json_str1
                    channel.basic_publish(exchange='',
                                           routing_key='Nagios-alert',
                                           body=body1)

                    # return PathData

        if key1 == MapMonitor:
            # continue
            print value1['services']
            for key2, value2 in value1['services'].items():
                print key2
                print value2
                if key2 in ['ArcGIS License Manager', 'ArcGIS Server',  'CPU Load','check-host-alive']:

                    hostname = key1
                    print hostname
                    services = key2
                    print services
                    state = nagiosstate[value2['current_state']]
                    print state

                    PathData = {
                        'hostname': str(hostname),
                        'services': str(services),
                        'state': str(state),
                    }
                    # 将相关状态信息以字典的形式存储
                    json_str1 = json.dumps(PathData)
                    body1 = json_str1
                    channel.basic_publish(exchange='',
                                          routing_key='Nagios-alert',
                                          body=body1)

                    # return PathData




info_store = (getinitmsg(initmsg))


#打印node-server状态信息
while True:
    # time_interval = 10
    # time.sleep(timesap)

    info_store_new = (getinitmsg(initmsg))



    print info_store_new
    pass


    getinitmsg(initmsg)



    time.sleep(10)


    #rabbitmq
    # json_str = json.dumps(PathData)
    src_data = info_store
    dst_data = info_store_new
    # cmp_diff(src_data,dst_data)








