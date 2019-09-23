#!/usr/bin/env python
# -*- coding: utf-8 -*-
#批量ping工具for windows，By ganxf

import os,time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
start_Time=int(time.time())
ip_True = open('ip_True.txt','w+')
ip_False = open('ip_False.txt','w+')
IPhost = []
IPbegin = (raw_input(unicode('请输入起始查询IP： ','utf-8').encode('gbk')))
IPend = raw_input(unicode('请输入终止查询IP： ','utf-8').encode('gbk'))
IP1 =  IPbegin.split('.')[0]
IP2 =  IPbegin.split('.')[1]
IP3 =  IPbegin.split('.')[2]
IP4 = IPbegin.split('.')[-1]
IPend_last = IPend.split('.')[-1]
count_True,count_False = 0,0
for i in range(int(IP4)-1,int(IPend_last)):
    ip = str(IP1+'.'+IP2+'.'+IP3+'.'+IP4)
    int_IP4 = int(IP4)
    int_IP4 += 1
    IP4 = str(int_IP4)
    return1=os.system('ping -n 4 -w 4 %s'%ip)
    if return1:
        print '\033[32mping %s is fail\033[0m'%ip
        ip_False.write(ip+'\n')
        count_False += 1
    else:
        print '\033[32mping %s is ok\033[0m'%ip
        ip_True.write(ip+'\n')
        count_True += 1
ip_True.close()
ip_False.close()
end_Time = int(time.time())
print u"\033[0;31mtime(秒)：\033[0m",end_Time - start_Time,"s"
print u"\033[0;31mping通的ip数：\033[0m",count_True,u"   \033[0;31mping不通的ip数：\033[0m",count_False
print u"请问你是否需要退出？"
i = 'n'
while  i != 'y':
    i = raw_input(unicode('请输入y/n：','utf-8').encode('gbk'))
