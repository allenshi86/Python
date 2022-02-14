import requests
import json
import subprocess
import time
import os
import datetime

#print(datetime.datetime.now())
##设备清单
devices = {
           '塔2-TEST1': '172.16.161.95',
           '塔2-TEST': '172.16.161.25'
          }


today = datetime.date.today()
localtime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
DATA = {'name': 'admin', 'pass': '9a3bdc603c940a18467d167af15d7894ci8c'}
HEADERS = {
    'Accept': 'application/json,text/javascript,*/*;q=0.01'
}

#目录创建
def directory_create():
    for directory  in devices.keys():
        path = "/Users/momo/Downloads/log/%s" % directory
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

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
                #print(r2)
                #print(r2['screenList'])
            with open("/Users/momo/Downloads/log/%s/%s.log" %(device,today),'a') as f:
                if r2['screenList'] != []:
                    f.write(r1['devicesName'] + ' ')
                    f.write(localtime + ' ')
                    f.write(str(r2['screenList']) + "\n")
         except Exception as e:
             pass
         continue

if __name__ == '__main__':
    directory_create()
    online_check()
    get_data()
