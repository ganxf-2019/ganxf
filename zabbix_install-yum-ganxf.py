#coding=utf-8
#From ganxf 2019-3-19
#Installed by CentOS 7.2

import subprocess
import getpass
import datetime
import time
import os
import sys


#####################################################################
#文件操作的类
class Edit_file(object):
    '''文件编辑的类'''

    def __init__(self ,file):
        self.file = file

    def copy_file(self, new_file):
        """拷备文件"""
        self.new_file = new_file
        f1 = open(self.file, "r")
        f2 = open(self.new_file, "w")
        content = f1.read()
        f2.write(content)
        f1.close()
        f2.close()

    def alter_str(self, old_str, new_str):
        '''按关键字修改文件内容'''
        self.old_str = old_str
        self.new_str = new_str
        f1 = open(self.file, "r")
        f2 = open("%s.new" %self.file,"w")
        for line in f1:
            if self.old_str in line:
                line = line.replace(self.old_str, self.new_str)
            f2.write(line)
        os.remove(self.file)
        os.rename("%s.new" %self.file, self.file)

    def alter_line(self, new_str, line_num):
        '''创建一个按行修改文件的函数'''
        self.new_str = new_str
        self.line_num = line_num
        with open(self.file, "r") as f:
            line = f.readlines()
            line[line_num-1] = self.new_str+"\n"
        with open(self.file, "w") as f:
            f.writelines(line)

    def str_line_num(self, str):
        '''判断字符是属于文件哪一行'''
        self.str = str
        num = 0
        f = open(self.file, "r")
        #a = f.readlines()
        s = f.read()
        a = s.split('\n')
        i = len(a)
        while num < i:
            if self.str in a[num]:
                line_num = num+1
                break
            num+=1
        return line_num

    def line_insert(self, line_num, new_str):
        '''创建一个在指定行添加内容的函数'''
        self.line_num = line_num
        self.new_str = new_str
        f = open(self.file, "r")
        s = f.read()
        f.close()
        a = s.split('\n')
        line_num = line_num-1
        a.insert(self.line_num, self.new_str)
        s = '\n'.join(a)
        f = open(self.file, "w")
        f.write(s)
        f.close()
####################################################################

#可执行shell命令的函数
def local_shell(cmd):
    '''执行shell命令并返回执行状态'''
    result = subprocess.call(cmd, shell=True)
    return result

###################################################################

#判断centos系统版本
def centos_ver():
    centos_version="cat /etc/issue | grep 6"
    Sver = local_shell(centos_version)
    return Sver

###################################################################


if __name__ == "__main__":
    #安装MySQLdb模块
    local_shell("yum -y install MySQL-python")
    import MySQLdb
    Sver = centos_ver()
    #判断zabbix_server是否安装
    zabbix_server_find = "cat /etc/passwd | grep zabbix"
    zabbix_server_exist = local_shell(zabbix_server_find) 
    if zabbix_server_exist == False:
        print "\033[32mzabbix_server服务已安装!!!\033[0m"
    else:
        if Sver:
            print("\033[32m当前可选择版本有2.2、3.0、3.2、3.4、3.5、4.0、4.1\033[0m")
            zabbix_ver = raw_input("\033[32m请输入需要安装的zabbix版本: \033[0m")
            zv_list = ['2.2', '3.0', '3.2', '3.4','3.5','4.0','4.1']
            while True:
                if zabbix_ver not in zv_list:
                    print("\033[31m所输版本号有误请重新输入!!!\033[0m")
                    zabbix_ver = raw_input("\033[32m请输入需要安装的zabbix版本\033[0m")
                else:
                    break
            if zabbix_ver == '4.1':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/4.1/rhel/7/x86_64/zabbix-release-4.1-1.el7.noarch.rpm"			
            elif zabbix_ver == '4.0':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm"
            elif zabbix_ver == '3.5':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/3.5/rhel/7/x86_64/zabbix-release-3.5-1.el7.noarch.rpm"
            elif zabbix_ver == '3.4':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm"
            elif zabbix_ver == '3.2':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm"
            elif zabbix_ver == '3.0':
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm"
            else:
                zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/2.2/rhel/7/x86_64/zabbix-release-2.2-1.el7.noarch.rpm"
            zabbix_install = "yum -y --enablerepo=zabbix --enablerepo=zabbix-non-supported install zabbix-server-mysql zabbix-web-mysql zabbix-agent mariadb mariadb-server"
            local_shell(zabbix_url)
            #zabbix4.1版本以下CentOS会出现gnutls-3.3版本过主的情况而不能启动服务
            if zabbix_ver == '4.1':
                local_shell(zabbix_install)
            else:
                gnutls_get = "wget ftp://mirror.switch.ch/pool/4/mirror/scientificlinux/7.0/x86_64/os/Packages/gnutls-3.1.18-8.el7.x86_64.rpm"
                local_shell(gnutls_get)
                local_shell("yum -y remove gnutls")
                local_shell("yum -y install gnutls-3.1.18-8.el7.x86_64.rpm")
                local_shell(zabbix_install)
            local_shell("systemctl start mariadb.service")
            local_shell("mysql_secure_installation")
            def mysql_login():
                sql_user = raw_input("\033[32m请输入Mysql用户名: \033[0m")
                sql_passwd = getpass.getpass("\033[32m请输密码: \033[0m")
                db = MySQLdb.connect(host="localhost", user=sql_user, passwd=sql_passwd, db="mysql", charset="utf8")
                return db
            try:
                db = mysql_login()
            except:
                print("\033[32m用户名密码有误，请重新输入!!!\033[0m")
                try:
                    db = mysql_login()
                except:
                    print("\033[32m用户名密码有误，请重新输入!!!\033[0m")
                    try:
                        db = mysql_login()
                    except:
                        print("\033[32m用户名密码连继三次有误，请检查用户名密码!!!\033[0m")
                        sys.exit()
            print("\033[36m已登录mysql...\033[0m")
            sql_zbdb = raw_input("\033[32m请输入新建zabbix数据库名: \033[0m")
            sql_zbuser = raw_input("\033[32m请输新建zabbix用户名: \033[0m")
            sql_zbpw = raw_input("\033[32m请输新建zaabix用户密码: \033[0m")
            cursor = db.cursor()    #创建一个游标对象
            cursor.execute("create database if not exists %s default charset utf8 collate utf8_bin;" %sql_zbdb)
            cursor.execute("grant all privileges on %s.* to %s@localhost identified by '%s';" %(sql_zbdb, sql_zbuser, sql_zbpw))
            db.close()
            if zabbix_ver != '2.2':
                sql_import = "zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -u"+sql_zbuser+" -p "+sql_zbdb
                local_shell(sql_import)
            else:
                sql_import1 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/schema.sql"
                sql_import2 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/images.sql"
                sql_import3 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/data.sql"
                local_shell(sql_import1)
                local_shell(sql_import2)
                local_shell(sql_import3)
            #########################################################################
            #修改配置文件
            os.chdir("/etc/zabbix/")
            zabbix = Edit_file("zabbix_server.conf")
            t = datetime.datetime.now().strftime('%Y-%m-%d')
            zabbix.copy_file("zabbix_server.conf.%s" %t)
            num1 = zabbix.str_line_num("# DBPassword=")
            num2 = num1+1
            num3 = num2+1
            zabbix.line_insert(num2, "")
            zabbix.line_insert(num3, "DBPassword=%s" %sql_zbpw)
            zabbix.alter_str("DBName=zabbix", "DBName=%s" %sql_zbdb)
            zabbix.alter_str("DBUser=zabbix", "DBUser=%s" %sql_zbuser)
            #关闭selinux
            os.chdir("/etc/selinux/")
            selinux = Edit_file("config")
            selinux.copy_file("config.%s" %t)
            selinux.alter_str("SELINUX=enforcing", "SELINUX=disabled")
            local_shell("setenforce 0")
            #修改httpd配置文件
            os.chdir("/etc/httpd/conf.d/")
            http_conf = Edit_file("zabbix.conf")
            http_conf.copy_file("zabbix.conf.%s" %t)
            http_conf.alter_str("        # php_value date.timezone Europe/Riga", "        php_value date.timezone Asia/Shanghai")
            ########################################################################
            zabbix_status = local_shell("systemctl start zabbix-server")
            local_shell("systemctl start zabbix-agent")
            local_shell("systemctl enable zabbix-server")
            local_shell("systemctl enable zabbix-agent")
            local_shell("systemctl start httpd")
            local_shell("systemctl enable mariadb")
            local_shell("systemctl enable httpd")
            local_shell("firewall-cmd --add-service=http --permanent")
            local_shell("firewall-cmd --add-port=10051/tcp --permanent")
            local_shell("firewall-cmd --reload")
            if zabbix_status == False:
                print("\033[32mzabbix_server安装成功!!!\033[0m")
            else:
                print("\033[32mzabbix_server安装失败!!!\033[0m")
        else:
            print("\033[32mCentOS6经测试只能成功安装2.2版本!!!\033[0m")
            zabbix_url = "rpm -ivh https://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm"
            zabbix_install = "yum -y --enablerepo=zabbix --enablerepo=zabbix-non-supported install zabbix-server-mysql zabbix-web-mysql zabbix-agent mysql mysql-server"
            local_shell(zabbix_url)
            local_shell(zabbix_install)
            local_shell("service mysqld start")
            local_shell("mysql_secure_installation")
            def mysql_login():
                sql_user = raw_input("\033[32m请输入Mysql用户名: \033[0m")
                sql_passwd = getpass.getpass("\033[32m请输密码: \033[0m")
                db = MySQLdb.connect(host="localhost", user=sql_user, passwd=sql_passwd, db="mysql", charset="utf8")
                return db
            try:
                db = mysql_login()
            except:
                print("\033[32m用户名密码有误，请重新输入!!!\033[0m")
                try:
                    db = mysql_login()
                except:
                    print("\033[32m用户名密码有误，请重新输入!!!\033[0m")
                    try:
                        db = mysql_login()
                    except:
                        print("\033[32m用户名密码连继三次有误，请检查用户名密码!!!\033[0m")
                        sys.exit()
            print("\033[36m已登录mysql...\033[0m")
            sql_zbdb = raw_input("\033[32m请输入新建zabbix数据库名: \033[0m")
            sql_zbuser = raw_input("\033[32m请输新建zabbix用户名: \033[0m")
            sql_zbpw = raw_input("\033[32m请输新建zaabix用户密码: \033[0m")
            cursor = db.cursor()    #创建一个游标对象
            cursor.execute("create database if not exists %s default charset utf8 collate utf8_bin;" % sql_zbdb)
            cursor.execute("grant all privileges on %s.* to %s@localhost identified by '%s';" %(sql_zbdb, sql_zbuser, sql_zbpw))
            db.close()
            sql_import1 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/schema.sql"
            sql_import2 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/images.sql"
            sql_import3 = "mysql -u"+sql_zbuser+" -p"+sql_zbpw+" "+sql_zbdb+" < /usr/share/doc/zabbix-server-mysql-2.2.22/create/data.sql"
            local_shell(sql_import1)
            local_shell(sql_import2)
            local_shell(sql_import3)
            #########################################################################
            #修改配置文件
            os.chdir("/etc/zabbix/")
            t = datetime.datetime.now().strftime('%Y-%m-%d')
            zabbix = Edit_file("zabbix_server.conf")
            zabbix.copy_file("zabbix_server.conf.%s" %t)
            num1 = zabbix.str_line_num("# DBPassword=")
            num2 = num1+1
            num3 = num2+1
            zabbix.line_insert(num2, "")
            zabbix.line_insert(num3, "DBPassword=%s" %sql_zbpw)
            zabbix.alter_str("DBName=zabbix", "DBName=%s" %sql_zbdb)
            zabbix.alter_str("DBUser=zabbix", "DBUser=%s" %sql_zbuser)
            #关闭selinux
            os.chdir("/etc/selinux/")
            selinux = Edit_file("config")
            selinux.copy_file("config.bak")
            selinux.alter_str("SELINUX=enforcing", "SELINUX=disabled")
            local_shell("setenforce 0")
            #修改httpd配置文件
            os.chdir("/etc/httpd/conf.d/")
            http_conf = Edit_file("zabbix.conf")
            http_conf.copy_file("zabbix.conf.%s" %t)
            http_conf.alter_str("        # php_value date.timezone Europe/Riga", "        php_value date.timezone Asia/Shanghai")
            #########################################################################
            zabbix_status = local_shell("service zabbix-server start")
            local_shell("service zabbix-agent start")
            local_shell("chkconfig --level 35 zabbix-server on")
            local_shell("chkconfig --level 35 zabbix-agent on")
            local_shell("service httpd start")
            local_shell("chkconfig --level 35  mysqld on")
            local_shell("chkconfig --level 35  httpd on")
            local_shell("iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT")
            local_shell("iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 10051 -j ACCEPT")
            local_shell("service iptables save")
            if zabbix_status == False:
                print("\033[32mzabbix_server安装成功!!!\033[0m")
            else:
                print("\033[32mzabbix_server安装失败!!!\033[0m")

print ("\033[32mzabbix安装完成后，须要修改图形显示字体，否则图形显示会有乱码出现。方法如下：cd /usr/share/zabbix/fonts/然后下载或者从windonws复制中文字体（例如simsun.tff）到以上目录，再执行vim /usr/share/zabbix/include/defines.inc.php进入后修改 define('ZBX_GRAPH_FONT_NAME',   'simsun') 这一行的simsun参数，其中simsun为想要改为的字体名称， :wq 保存退出后，重启httpd服务，登陆zabbix即可图形显示正常。\033[0m")
print ("\033[0;31mzabbix默认用户名为：Admin\033[0m")
print ("\033[0;31mzabbix默认密码为：zabbix\033[0m")
print ("\033[0;31m安装完成后，添加主机须要修改/etc/zabbix/zabbix_server.conf文件中的“StatsAllowedIP=127.0.0.1,在此逗号后添加zabbix server的主机实际ip”\033[0m")
print ("\033[0;31m安装完成后，添加主机须要修改/etc/zabbix/zabbix_agentd.conf文件中的“Hostname=Zabbix server”选项\033[0m")