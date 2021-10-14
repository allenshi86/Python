#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import os
import re
import pymysql
ap_online = {}  #存储在线AP, key为ap_id，value为ap_name

ap_status_oid = '.1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.19'
ap_name_oid = '1.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.3'

#获取AP名称和唯一标识,存入ap_info

def get_all_ap():
    ap_info_datas = os.popen('snmpwalk  -v 2c -c Hjc4QPaRZXPbJ 172.16.202.8 {}'.format(ap_name_oid))
    ap_info_lists = ap_info_datas.read().splitlines()
    for temp in ap_info_lists:
        ap_name = "".join(re.findall(r'"(.+)"', temp))
        ap_id = "".join(re.findall(r"1.3.(.+) =", temp))
        ap_online['{}'.format(ap_id)] = ap_name


#过滤掉不在线的AP
def offline_ap_filter():
    ap_status_datas = os.popen('snmpwalk  -v 2c -c Hjc4QPaRZXPbJ 172.16.202.8 {} | grep "INTEGER: 2"'.format(ap_status_oid))
    ap_status_lists = ap_status_datas.read().splitlines()
    for temp in ap_status_lists:
        offline_ap_id = "".join(re.findall(r"1.19.(.+) =", temp))
        del ap_online['{}'.format(offline_ap_id)]

if __name__ == '__main__':
    get_all_ap()
    offline_ap_filter()
    print(ap_online)



