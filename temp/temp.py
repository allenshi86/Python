import os
import re

'''
data = os.popen('snmpwalk  -v 2c -c Hjc4QPaRZXPbJ 172.16.202.9 1.3.6.1.4.1.14823.2.2.1.5.2.1.5.1.6.72.74.233.194.255.78').read()

x = re.findall(r'1.6.(.+).78', data)

print(x)
'''

#a= int(10)
#print(10/2.format(.))

#wlc_ip = ["172.16.202.8", "172.16.202.9"]

#for i in wlc_ip:
 #   print(type(i))
'''
oid = '.1.3.6.1.4.1.14823.2.2.1.4.1.2.1.10'
ap_dict = {}

data = os.popen('snmpwalk -v 2c -c Hjc4QPaRZXPbJ 172.16.202.8 %s' % oid).read().splitlines()
for temp in data:
    ap_name = ''.join(re.findall(r'"(.+)"', temp))
    ap_user_id = ''.join(re.findall(r'.1.10.(.+?) =', temp))
    user_ip = ''.join(re.findall(r'(1[7|9]2.168?.\d+.\d+)', ap_user_id))
    print(user_ip)
 #   print(ap_name)
 #   print(ap_user_id)
  #  ap_dict[ap_user_id] = ap_name
 #   users_data = os.popen('snmpwalk -v 2c -c Hjc4QPaRZXPbJ %s %s.%s' % (ip, oid_userName, ap_user_id)).read()
 #   user = ''.join(re.findall(r'"(.+)"', users_data))
'''

tup = ('t1-f16-ap01')

print("".join(tup))
