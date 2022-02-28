import requests
import json
import subprocess
import time
import os
import datetime
import pymysql

#设备清单
devices = {

###会议室
           '塔1-16层-1会': '172.16.xxx.xxx',
           '塔1-16层-2会': '172.16.xxx.xxx',
 
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
            db = pymysql.connect(host='172.16.7.3xx', user='wxtp01', password='M2016', database='wxtouping')
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
