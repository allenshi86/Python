#!/bin/bash

for email in `cat list`
do
  groups=`/opt/zimbra/bin/zmprov gam $email |grep -v 'via'|grep 'tantanapp.com'`
  #echo $groups
  for group in ${groups[@]}
  do
     /opt/zimbra/bin/zmprov gam $email |grep -v 'via'| grep 'tantanapp.com'
     if [[ $? -eq 0 ]];then
        /opt/zimbra/bin/zmprov rdlm $group $email
     fi
     
  done 
done
