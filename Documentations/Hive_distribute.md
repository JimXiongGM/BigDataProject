# Hive分布式环境搭建




## 安装MySQL

sudo apt-get install -y mysql-server

配置用户名密码
首先我们以root身份登录到mysql服务器：

sudo mysql -u root
然后修改root的密码，并允许root远程访问：

GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY "123456";
我们这里还可以为hive建立一个用户，而不是用root用户：

GRANT ALL PRIVILEGES ON *.* TO hive@'%' IDENTIFIED BY "hive";
运行完成后quit命令即可退出mysql的命令行模式。


## 配置远程访问
默认情况下，MySQL是只允许本机访问的，要允许远程机器访问需要修改配置文件

sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
找到bind-address的配置部分，然后改为：

bind-address          = 0.0.0.0


sed -i '/bind-address/'d /etc/mysql/mysql.conf.d/mysqld.cnf;
echo 'bind-address          = 0.0.0.0' >> /etc/mysql/mysql.conf.d/mysqld.cnf;


保存，重启mysql服务

sudo service mysql restart
重启完成后，我们可以在Windows下，用MySQL的客户端连接master上的MySQL数据库，看是否能够远程访问。




















cd /root/xiazai;
wget http://mirror.bit.edu.cn/apache/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz;

tar -zxvf apache-hive-3.1.1-bin.tar.gz;

mv apache-hive-3.1.1-bin /opt/hive-3.1.1;

echo '
# HIVE SETTINGS
export HIVE_HOME=/opt/spark-2.4.0
export PATH=$HIVE_HOME/bin:$PATH
' >> /etc/bash.bashrc ;
source /etc/bash.bashrc;




