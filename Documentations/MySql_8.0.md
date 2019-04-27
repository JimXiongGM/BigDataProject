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

## <p id=2>增加用户

新增用户并授权

`$ mysql -u root -p` 
```sql      
create user 'xiong'@'%' identified by 'xiong';
create user 'guest'@'%' identified by 'guest';
GRANT ALL PRIVILEGES ON *.* TO 'xiong'@'%';
GRANT SELECT ON *.* TO 'guest'@'%';
SELECT HOST,USER,SELECT_PRIV, INSERT_PRIV, UPDATE_PRIV,DELETE_PRIV,CREATE_PRIV,DROP_PRIV FROM USER;
show grants for 'xiong';
```


## <p id=3>新建数据库

`$ mysql -u xiong -p` 

```sql
CREATE DATABASE xiong_db CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE xiong_db;
CREATE TABLE test01 (
        testid VARCHAR(256) NOT NULL PRIMARY KEY,
        tesename VARCHAR(256) NOT NULL       
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```


## <p id=4>远程访问

`$ mysql -u root -p`
```sql
use mysql;
select host,user,authentication_string,plugin from user;
update user set host='%' where user='root';
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




