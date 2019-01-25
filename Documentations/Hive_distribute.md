# Hive分布式环境搭建

本文前提需要配置好hadoop分布式环境，无需HA。

本文主要参考[网络资料](https://www.cnblogs.com/studyzy/p/setup-hive.html)

## 目录

- [安装MySQ](#1)
- [配置远程访问](#2)
- [配置环境变量](#3)
- [配置文件](#4)
- [下载MySQL JDBC驱动](#5)
- [初始化](#6)
- [使用hive](#7)
- [测试](#8)


## <p id=1>安装MySQL

首先以root身份登录到mysql服务器，配置用户名密码，并允许root远程访问。

为hive建立一个用户，密码为hive。运行完成后quit命令即可退出mysql的命令行模式。

```
sudo apt-get install -y mysql-server;
sudo mysql -u root;
GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY "123456";
GRANT ALL PRIVILEGES ON *.* TO hive@'%' IDENTIFIED BY "hive";
```

## <p id=2>配置远程访问

默认情况下，MySQL是只允许本机访问的，要允许远程机器访问需要修改配置文件，然后重启服务。
```
sed -i '/bind-address/'d /etc/mysql/mysql.conf.d/mysqld.cnf;
echo 'bind-address          = 0.0.0.0' >> /etc/mysql/mysql.conf.d/mysqld.cnf;
sudo service mysql restart;
```

## <p id=3>配置环境变量

没什么好说
```
cd /root/xiazai;
wget http://mirror.bit.edu.cn/apache/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz;
tar -zxvf apache-hive-3.1.1-bin.tar.gz;
mv apache-hive-3.1.1-bin /opt/hive-3.1.1;

echo '
# HIVE SETTINGS
export HIVE_HOME=/opt/hive-3.1.1
export PATH=$HIVE_HOME/bin:$PATH
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib:$HIVE_HOME/lib
' >> /etc/bash.bashrc ;
source /etc/bash.bashrc;
```


## <p id=4>配置文件

这里要配置3个文件。

从本项目下拷贝hive-site.xml到master。hive-site.xml需要修改的部分已经列在文件最前面。
`scp ./Documentations/Hive_config_files/conf/hive-site.xml root@master:/opt/hive-3.1.1/conf/`
```
echo '已从本地拷贝hive-site.xml';
mv $HIVE_HOME/conf/hive-default.xml.template $HIVE_HOME/conf/hive-default.xml.template.BACKUP;
mkdir -p /home/hduser/iotmp;

echo '编辑hive-env.sh';
cp $HIVE_HOME/conf/hive-env.sh.template $HIVE_HOME/conf/hive-env.sh;
echo "HADOOP_HOME=$HADOOP_HOME" >> $HIVE_HOME/conf/hive-env.sh;

echo '编辑hive-config.sh';
echo "
# xgm add
export JAVA_HOME=$JAVA_HOME
export HADOOP_HOME=$HADOOP_HOME
export HIVE_HOME=$HIVE_HOME
" >> $HIVE_HOME/bin/hive-config.sh;

echo '解决WARN SLF4J: Class path contains multiple SLF4J bindings.';
mv /opt/hive-3.1.1/lib/log4j-slf4j-impl-2.10.0.jar /opt/hive-3.1.1/lib/log4j-slf4j-impl-2.10.0.jar.BACKUP;
```

## <p id=5>下载MySQL JDBC驱动

去MySQL的官网，https://dev.mysql.com/downloads/connector/j/  下载JDBC驱动到master服务器上。
```
cd /root/xiazai/;
wget https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-5.1.47.tar.gz;
tar -zxvf mysql-connector-java-5.1.47.tar.gz;
cp ./mysql-connector-java-5.1.47/*.jar $HIVE_HOME/lib/;
```

## <p id=6>初始化

```
hadoop fs -mkdir /tmp;
hadoop fs -mkdir -p /user/hive/warehouse;
hadoop fs -chmod g+w /tmp;
hadoop fs -chmod g+w /user/hive/warehouse;
$HIVE_HOME/bin/schematool -initSchema -dbType mysql --verbose;
```

## <p id=7>使用hive

输入`hive`
```
show databases;
show tables;
```

输出如下
```bash
root@master:~# hive
...
...
...
Hive Session ID = 28bc7cce-8668-422d-9640-03fdcaa0e6c6
hive> show databases;
OK
default
Time taken: 0.797 seconds, Fetched: 1 row(s)
hive> show tables;
OK
Time taken: 0.04 seconds
hive> quit;
```

## <p id=8>测试

创建一个测试文件，使用`|`分隔列。
```
touch /root/xiazai/UsersTEST_01.txt;
echo '2|Edward 
3|Mindy 
4|Dave 
5|Joseph 
6|Leo' > /root/xiazai/UsersTEST_01.txt;
hive
```

新建表，从txt中读取数据，增加字段并且查询数据。
```sql
create table UsersTEST (ID int,Name String) ROW FORMAT DELIMITED FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INPATH '/root/xiazai/UsersTEST_01.txt' into table UsersTEST ;
select * from UsersTEST ;
select * from UsersTEST where Name like 'D%';

-- 增加字段BirthDate
alter table UsersTEST add columns (BirthDate date);

-- 查询表定义
desc UsersTEST;

-- 重命名表
alter table UsersTEST rename to StudentTEST;
select * from StudentTEST ;

truncate table StudentTEST;
```

输出如下
```sql
hive> create table UsersTEST (ID int,Name String) ROW FORMAT DELIMITED FIELDS TERMINATED BY '|';
OK
Time taken: 0.119 seconds
hive> LOAD DATA LOCAL INPATH '/root/xiazai/UsersTEST_01.txt' into table UsersTEST ;
Loading data to table default.userstest
OK
Time taken: 0.33 seconds
hive> select * from UsersTEST ;
OK
2       Edward
3       Mindy
4       Dave
5       Joseph
6       Leo
Time taken: 0.26 seconds, Fetched: 5 row(s)
hive> select * from UsersTEST where Name like 'D%';
OK
4       Dave
Time taken: 0.264 seconds, Fetched: 1 row(s)
hive>
    > -- 增加字段BirthDate
    > alter table UsersTEST add columns (BirthDate date);
OK
Time taken: 0.157 seconds
hive>
    > -- 查询表定义
    > desc UsersTEST;
OK
id                      int
name                    string
birthdate               date
Time taken: 0.091 seconds, Fetched: 3 row(s)
hive>
    > -- 重命名表
    > alter table UsersTEST rename to StudentTEST;
FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. Unable to alter table. new table default.studenttest already exists
hive> select * from StudentTEST ;
OK
2       Edward  NULL
3       Mindy   NULL
4       Dave    NULL
5       Joseph  NULL
6       Leo     NULL
Time taken: 0.24 seconds, Fetched: 5 row(s)
hive> quit;
```
