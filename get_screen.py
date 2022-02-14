import requests
import json
import subprocess
import time
import os
import datetime
import pymysql

#设备清单
devices = {
###高管
           '塔2-20层-TY': '172.16.161.14',
           '塔2-20层-CFO': '172.16.161.12',
           '塔2-20层-WL': '172.16.161.17',
           '塔2-11层-JW': '172.16.161.13',
           '塔2-11层-CTO': '172.16.161.15',
           '塔3-19层-DW': '172.16.161.11',
###投影
           '塔2-20层-1会': '172.16.161.19',
           '塔2-20层-8会': '172.16.161.18',
           '塔2-20层-9会': '172.16.161.20',
           '塔2-11层-21会': '172.16.161.21',
           '塔2-11层-27会': '172.16.161.23',
           '塔2-11层-29会': '172.16.161.22',
           '塔1-16层-6会': '172.16.161.24',
           '塔1-16层-10会': '172.16.161.10',
           '塔3-19层-10会': '172.16.161.26',
           '塔3-30层-3会': '172.16.161.27',
###会议室
           '塔1-16层-1会': '172.16.161.29',
           '塔1-16层-2会': '172.16.161.31',
           '塔1-16层-3会': '172.16.161.41',
           '塔1-16层-4会': '172.16.161.35',
           '塔1-16层-5会': '172.16.161.38',
           '塔1-16层-7会': '172.16.161.37',
           '塔1-16层-8会': '172.16.161.36',
           '塔1-16层-9会': '172.16.161.34',
           '塔1-16层-11会': '172.16.161.33',
           '塔1-16层-13会': '172.16.161.30',
           '塔2-19层-13会': '172.16.161.50',
           '塔2-19层-14会': '172.16.161.53',
           '塔2-19层-15会': '172.16.161.43',
           '塔2-19层-16会': '172.16.161.42',
           '塔2-19层-17会': '172.16.161.54',
           '塔2-20层-3会': '172.16.161.51',
           '塔2-20层-4会': '172.16.161.45',
           '塔2-20层-5会': '172.16.161.55',
           '塔2-20层-6会': '172.16.161.52',
           '塔2-20层-11会': '172.16.161.56',
           '塔2-20层-12会': '172.16.161.57',
           '塔2-20层-18会': '172.16.161.58',
           '塔3-19层-8会': '172.16.161.39',
           '塔3-19层-9会': '172.16.161.59',
           '塔3-19层-12会': '172.16.161.60',
           '塔3-19层-13会': '172.16.161.49',
           '塔3-30层-1会': '172.16.161.61',
           '塔3-30层-2会': '172.16.161.47',
           '塔3-30层-4会': '172.16.161.62',
           '塔3-30层-5会': '172.16.161.44',
           '塔3-30层-6会': '172.16.161.63',
           '塔3-30层-7会': '172.16.161.32'
          }


localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
DATA = {'name': 'admin01', 'pass': '9a3bdc603c67d167af21536'}
HEADERS = {
    'Accept': 'application/json,text/javascript,*/*;q=0.01'
}
print(localtime)
#检查设备在线情况，只对在线设备索取数据
online_devives = {}
def online_check():
    for device in devices.keys():
        ip = devices[device]
        text = os.popen("/usr/local/bin/fping %s" % ip)
        res = list(text.read().rstrip().split(" "))
        if "alive" in res:
            online_devives[device] = ip


def login(url):
    req = requests.post(url, json=DATA, headers=HEADERS)
    #import pdb; pdb.set_trace()
    token = req.json()["token"]
    return token

def get_data():
     for device in online_devives.keys():
         try:
            LOGIN_URL = "http://%s/oam/doLogin.fcgi" % devices[device]
            SYSINFO_URL = "http://%s/SystemInfo.fcgi" % devices[device]
            SCREENINFO_URL = "http://%s/screenStatu.fcgi" % devices[device]
            token = login(LOGIN_URL)
            r1 = requests.post(url=SYSINFO_URL, json={'token': token})
            r2 = requests.post(url=SCREENINFO_URL, json={'token':token})
#               print(r1.status_code)
            r1.encoding,r2.encoding = 'utf8','utf8'
            r1 = eval(r1.text)
            r2 = eval(r2.text)
            client_ip = r2['screenList'][0]['ip']
            client_hostname = r2['screenList'][0]['sendername']
            client_screen_type = r2['screenList'][0]['type']
            client_duation = r2['screenList'][0]['duation']
            db = pymysql.connect(host='172.16.7.33', user='wxtp', password='Momo.20!6', database='wxtouping')
            cursor = db.cursor()
            cursor.execute("INSERT INTO wuxtp VALUES (%s,%s,%s,%s,%s)",(device,client_ip,client_hostname,client_screen_type,client_duation))
            db.commit()
#            cursor.execute("select * from wuxtp")
#            data = cursor.fetchall()
            db.close()
         except Exception as e:
             pass
         continue

if __name__ == '__main__':
    online_check()
    get_data()
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(localtime)
