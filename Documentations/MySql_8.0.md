# MySQL8.0环境搭建

MySQL8.0采用强加密方式，并且在新增用户、用户授权等方面有不一样的命令格式。

## 目录

- [安装](#1)
- [增加用户](#2)
- [新建数据库](#3)
- [远程访问](#4)
- [改变加密方式](#5)
- [操作数据库](#6)
- [ubuntu基本操作](#7)
- [与spark交互组件安装](#8)
- [重置数据库](#9)
- [卸载MYSQL](#10)

## <p id=1>安装

```bash
cd xiazai;
wget https://repo.mysql.com//mysql-apt-config_0.8.12-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.12-1_all.deb

选择对应的系统并选择ok

sudo apt update;
sudo apt-get install -y mysql-server;
sudo apt-get install -y libmysqlclient-dev;
pip3 install mysqlclient;
```

测试连接
```
mysql -u root -p
```

测试命令
```
show variables like '%char%'; 
```


## <p id=3>新建数据库

`$ mysql -u root -p` 

```sql
CREATE DATABASE xionggm_db;
USE xionggm_db;
CREATE TABLE test01 (
        testid VARCHAR(256) NOT NULL PRIMARY KEY,
        tesename VARCHAR(256) NOT NULL       
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## <p id=2>增加用户并赋予对应数据库权限

新增用户并授权

`$ mysql -u root -p` 
```sql      
create user 'xiong'@'%' identified by 'Xiong123';
GRANT ALL PRIVILEGES ON xionggm_db TO 'xiong'@'%';

create user 'guest'@'%' identified by 'guest';
GRANT SELECT ON *.* TO 'guest'@'%';

use mysql;
SELECT HOST,USER,SELECT_PRIV, INSERT_PRIV, UPDATE_PRIV,DELETE_PRIV,CREATE_PRIV,DROP_PRIV FROM user;
show grants for 'xiong';

```


## <p id=4>远程访问

**不建议开放root用户的远程访问权限**

`$ mysql -u root -p`
```sql
use mysql;
select host,user,authentication_string,plugin from user;
update user set host='172.17.%.%' where user='root';
flush privileges;
```

改回去
```sql
use mysql;
select host,user,authentication_string,plugin from user;
update user set host='localhost' where user='root';
flush privileges;
```

## <p id=5>改变加密方式

- 改为弱加密

```sql
ALTER USER 'root'@'%' IDENTIFIED BY 'mysql' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'mysql';
FLUSH PRIVILEGES;
```

- 改回强加密

```sql
ALTER USER 'root'@'%' IDENTIFIED WITH caching_sha2_password BY 'mysql';
FLUSH PRIVILEGES;
```

## <p id=6>操作数据库

```sql
show databases;
create database xgmdb;
drop database xgmdb;
```

## <p id=7>ubuntu基本操作

```bash
service mysql start
service mysql stop
service mysql status
```

## <p id=8>与spark交互组件安装

```bash
cd xiazai;
wget http://central.maven.org/maven2/mysql/mysql-connector-java/8.0.15/mysql-connector-java-8.0.15.jar;
mv mysql-connector-java-8.0.15.jar $SPARK_HOME/jars
echo "
# MYSQL JARS SETTINGS
export EXTRA_SPARK_CLASSPATH=$SPARK_HOME/jars
" >> $SPARK_HOME/conf/spark-env.sh;

scp mysql-connector-java-8.0.15.jar root@slave1:$SPARK_HOME/jars;
scp mysql-connector-java-8.0.15.jar root@slave2:$SPARK_HOME/jars;
scp mysql-connector-java-8.0.15.jar root@slave3:$SPARK_HOME/jars;
scp $SPARK_HOME/conf/spark-env.sh root@slave1:$SPARK_HOME/conf/;
scp $SPARK_HOME/conf/spark-env.sh root@slave2:$SPARK_HOME/conf/;
scp $SPARK_HOME/conf/spark-env.sh root@slave3:$SPARK_HOME/conf/;
stop-all.sh;start-all.sh
```


## <p id=9>重置数据库

进入mysql：`mysql -u root -p`

- 删库
```sql
drop database MovieSizer;
drop database PLEASE_READ_ME_XMG;
drop database cuipz;
drop database mysql;
drop database scrapy_db;
drop database tripadvisor_mch;
drop database xgm;
```

- 查询并删除用户
```sql
USE mysql;
SELECT USER FROM user;
...
DROP ROLE 'guest','mch','mysqlbackups','xiong','guest','mysql';
-- 上述语句遇到错误，使用如下语句。
-- ERROR 1227 (42000): Access denied; you need (at least one of) the SYSTEM_USER privilege(s) for this operation
delete from user where user = 'xiong';
delete from user where user = 'guest';
delete from user where user = 'mysql';
```

- 修改密码
```sql
alter user'root'@'%' IDENTIFIED BY 'Mysql_08'; 
```

- 修改端口并重启服务
```bash
service mysql stop;
echo'
# overwrite default port
port = 3308
' >> /etc/mysql/mysql.conf.d/mysqld.cnf;
service mysql start;
service mysql status;
```

## <p id=10>卸载MYSQL

使用`sudo apt-get remove --purge mysql-\*`一键卸载，使用`sudo find  / -name mysql -print`查询残余目录，使用`rm -rf`卸载。