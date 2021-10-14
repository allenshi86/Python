#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import re
import pymysql
import time
import push_ap

ap_name_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.3'
ap_radio_clients_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.5.1.7'
ap_channel_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.5.1.6'
prefix_double5G_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.48'
ap_status_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.19'

ap_double_5G = {}       #开启双5G的AP列表.开启双5G的AP,radio0客户端数量准确，radio1的客户端数量需要除以2.

ap_single_5G = {}       #禁用双5G的AP列表.


def get_double_5G(dict):
    for ap_id in dict.keys():
        datas = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s' % (prefix_double5G_oid, ap_id)).read()
        value = int(datas.split(':')[-1])
        if value == 1:       #值为1，已启用双5G.值为0，未启用.
            ap_double_5G[ap_id] = dict[ap_id]

def get_single_5G(dict):
    for ap_id in dict.keys():
        if ap_id not in ap_double_5G.keys():
            ap_single_5G[ap_id] = dict[ap_id]

timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())


def get_apdata_single5G(dict):
    for ap_id in dict.keys():
        try:
            datas = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s' % (ap_channel_oid, ap_id)).read()
            if not re.findall(r'No Such Instance',datas):
                ap_radio0_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.2' % (ap_channel_oid, ap_id)).read().split(':')[-1] #raido0 为2.4G
                ap_radio1_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.1' % (ap_channel_oid, ap_id)).read().split(':')[-1] #raido1 为5G
                ap_client_number_radio0 = int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.2' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
                ap_client_number_radio1 = int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.1' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
            else:
                ap_radio0_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.2' % (ap_channel_oid, ap_id)).read().split(':')[-1] #raido0 为2.4G
                ap_radio1_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.1' % (ap_channel_oid, ap_id)).read().split(':')[-1] #raido1 为5G
                ap_client_number_radio0 = int(os.popen('snmpwalk -v 2c -c Hjc4172.16.202.9 %s.%s.2' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
                ap_client_number_radio1 = int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.1' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
            ap_client_number = ap_client_number_radio0 + ap_client_number_radio1
#将数据可入数据库
            db = pymysql.connect(host='127.0.0.1', user='root', password='momo2021', database='momo')
            cursor = db.cursor()
            cursor.execute("INSERT INTO ap_apdata (ap_name,query_time,ap_radio0_usage,ap_radio1_usage,ap_client_number_radio0,ap_client_number_radio1,ap_client_number) VALUES (%s,%s,%s,%s,%s,%s,%s)",(dict[ap_id], timenow, ap_radio0_usage, ap_radio1_usage, ap_client_number_radio0, ap_client_number_radio1, ap_client_number))
            db.commit()
            db.close()
        except Exception as e:
            pass
        continue

def get_apdata_double5G(dict):
    for ap_id in dict.keys():
        try:
            datas = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s' % (ap_channel_oid, ap_id)).read()
            if not re.findall(r'No Such Instance', datas):
                ap_radio0_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.2' % (ap_channel_oid, ap_id)).read().split(':')[-1]  # raido0 为2.4G
                ap_radio1_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.1' % (ap_channel_oid, ap_id)).read().split(':')[-1]  # raido1 为5G
                ap_client_number_radio0 = int(int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.2' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1]) / 2)
                ap_client_number_radio1 = int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.8 %s.%s.1' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
            else:
                ap_radio0_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.2' % (ap_channel_oid, ap_id)).read().split(':')[-1]  # raido0 为2.4G
                ap_radio1_usage = os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.1' % (ap_channel_oid, ap_id)).read().split(':')[-1]  # raido1 为5G
                ap_client_number_radio0 = int(int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.2' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1]) / 2)
                ap_client_number_radio1 = int(os.popen('snmpwalk -v 2c -c Hjc4 172.16.202.9 %s.%s.1' % (ap_radio_clients_oid, ap_id)).read().split(':')[-1])
#                print(dict[ap_id],ap_client_number_radio0)
#                print(dict[ap_id],ap_client_number_radio1)
            ap_client_number = ap_client_number_radio0 + ap_client_number_radio1
# 将数据可入数据库
            db = pymysql.connect(host='127.0.0.1', user='root', password='momo2021', database='momo')
            cursor = db.cursor()
            cursor.execute("INSERT INTO ap_apdata (ap_name,query_time,ap_radio0_usage,ap_radio1_usage,ap_client_number_radio0,ap_client_number_radio1,ap_client_number) VALUES (%s,%s,%s,%s,%s,%s,%s)",(dict[ap_id], timenow, ap_radio0_usage, ap_radio1_usage, ap_client_number_radio0, ap_client_number_radio1, ap_client_number))
            db.commit()
            db.close()
        except Exception as e:
            pass
        continue

if __name__ == '__main__':
    push_ap.get_all_ap()
    push_ap.offline_ap_filter()
    get_double_5G(push_ap.ap_online)
    get_single_5G(push_ap.ap_online)
    get_apdata_double5G(ap_double_5G)
    get_apdata_single5G(ap_single_5G)
    print(ap_single_5G)




