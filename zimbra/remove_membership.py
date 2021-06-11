#!/usr/bin/env python

import os

groups=['employees-trainee@tantanapp.com','qa-wb@tantanapp.com','employees-wb@tantanapp.com']

users = os.popen('cat list').read().split()
for user in users:
   #print user
   for group in groups:
       if os.system("/opt/zimbra/bin/zmprov gam %s | grep -i %s" %(user,group) ) == 0:
           os.system("/opt/zimbra/bin/zmprov rdlm %s %s" %(group,user))
