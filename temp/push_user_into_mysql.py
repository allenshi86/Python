#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import re
import pymysql
import time
import push_ap

oid_userAPLocation = '.1.3.6.1.4.1.14823.2.2.1.4.1.2.1.10'
oid_userName = '.1.3.6.1.4.1.14823.2.2.1.4.1.2.1.3'

ap_dict = {}
wlc_ip = ['172.16.202.8', '172.16.202.9']

localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def get_user_data(ip_list):
    for ip in ip_list:
        data = os.popen('snmpwalk -v 2c -c Hjc4 %s %s' % (ip, oid_userAPLocation)).read().splitlines()
#        print(data)
        for temp in data:
            ap_name = ''.join(re.findall(r'"(.+)"', temp))
            ap_user_id = ''.join(re.findall(r'1.10.(.+?) =', temp))
            user_ip = ''.join(re.findall(r'(1[7|9]2.168?.\d+.\d+)', ap_user_id))
            #print(user_id)
            ap_dict[ap_user_id] = ap_name
            users_data = os.popen('snmpwalk -v 2c -c Hjc4 %s %s.%s' % (ip, oid_userName, ap_user_id)).read()
            user = ''.join(re.findall(r'"(.+)"', users_data))
            if not user:
                user = 'NONE'
#            print(user_ip)
#            print(ap_name)
#            print('---')
#            print(ap_name,user_ip, user)
            db = pymysql.connect(host='127.0.0.1', user='root', password='momo2021', database='momo')
            cursor = db.cursor()
            cursor.execute("insert into ap_apinfo (user,user_ip,ap_name,cap_time) VALUES (%s,%s,%s,%s)", (user, user_ip, ap_name, localtime))
            db.commit()
            db.close()

if __name__ == '__main__':
    get_user_data(wlc_ip)



