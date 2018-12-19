# MongoDB的本地安装+PyMongo的基本操作


> [本地部署](#1)  
> [PyMongo的基本操作](#2)


## <p id=1>本地部署</p>

本文参考自官网安装教程，[点击这里](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu-tarball/).  

从官网下载MongoDB编译好的tgz压缩文件，[点击这里](https://www.mongodb.com/download-center/community?jmp=docs)，选择对应的version、OS、package并下载。注意不能点击右侧Download source (tgz)，那个是下载源码。  

本文使用的下载链接是[这个](https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.0.4.tgz)。使用`tar -zvxf mongodb-linux-x86_64-ubuntu1804-4.0.4.tgz -C /usr/local/mongodb`解压文件到指定文件夹  

在`~/.bashrc`中添加环境变量。关于/etc/profiel、~/.bashrc等的区别，[点击这里](https://www.cnblogs.com/liduanjun/p/3536993.html)。

打开`sudo gedit ~/.bashrc`

添加
```js
export MONGODB_HOME=/usr/local/mongodb/mongodb-linux-x86_64-ubuntu1804-4.0.4
export PATH=$MONGODB_HOME/bin:$PATH
```
生效  
`source ~/.bashrc`

确认环境变量  
`echo $MONGODB_HOME`

创建存放data的目录。根据官网介绍，/data/db 是 MongoDB 默认的启动的数据库路径。这里我使用自定义路径  
`sudo mkdir -p /home/mongodb/data`

创建日志存放目录。  
`sudo mkdir -p /home/mongodb/logs`
  
在$MONGODB_HOME/bin下有mongo文件，我们可以进入并启动   
`mongod --dbpath /home/mongodb/data --logpath /home/mongodb/logs/mongod.log --fork`

可以看到产生错误  
```s
xgm@xgm-xps:/usr/local/mongodb/mongodb-linux-x86_64-ubuntu1804-4.0.4/bin$ mongod --dbpath /home/mongodb/data --logpath /home/mongodb/logs/mongod.log
2018-12-10T20:34:49.799+0800 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-12-10T20:34:49.799+0800 F CONTROL  [main] Failed global initialization: FileNotOpen: Failed to open "/home/mongodb/logs/mongod.log"
```
很明显是没有权限，因此我们应该使用root账户进行操作。  
先将上述环境变量添加到/etc/profile  
```
su
gedit /etc/profile
source /etc/profile
echo $MONGODB_HOME
mongod --dbpath /home/mongodb/data --logpath /home/mongodb/logs/mongod.log --fork  
```


可以看到，此时控制台输出：
```s
root@xgm-xps:/home/xgm# mongod --dbpath /home/mongodb/data --logpath /home/mongodb/logs/mongod.log --fork
2018-12-10T20:39:31.391+0800 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
about to fork child process, waiting until server is ready for connections.
forked process: 25230
child process started successfully, parent exiting
```
至此成功启动。根据官网，首先我们看看相应日志文件。  
`cat /home/mongodb/logs/mongod.log`

我们可以在输出中找一找这一句：  
`2018-12-10T20:39:32.177+0800 I NETWORK  [initandlisten] waiting for connections on port 27017`  

“只要看到这一句，我们可以放心地不用顾虑那些不重要的warnings”  
> You may see non-critical warnings in the process output. As long as you see the log line shown above, you can safely ignore these warnings during your initial evaluation of MongoDB.

同样，我们可以通过查看端口占用情况，确认其在运行  
`netstat -a | grep 27017`  

输出为  
```
root@xgm-xps:/home# netstat -a | grep 27017
tcp        0      0 localhost:27017         0.0.0.0:*               LISTEN     
unix  2      [ ACC ]     流        LISTENING     699135   /tmp/mongodb-27017.sock
```

然后我们可以直接使用`mongo`命令，进入shell，使用`exit`，退出shell。  

关于shell的使用，我们可以参考[官网](https://docs.mongodb.com/manual/mongo/)，以及[菜鸟教程](http://www.runoob.com/mongodb/mongodb-create-database.html)。

本文直接使用Python3操作MongoDB。  

## <p id=2>PyMongo的基本操作</p>  

本文使用Python3进行编写，首先我们要安装pip3，并且安装相应pymongo  
`sudo apt-get install python3-pip`
`pip3 install pymongo`

详情可见`MongDBWithCrawler`目录下[hello_mongodb.py](../MongDBWithCrawler/hello_mongodb.py)

pymongo的快速指南在[这里](https://api.mongodb.com/python/current/tutorial.html)，本章实例代码就是从获取。
pymongo的CURD命令与SQL相对应的部分在[这里](https://docs.mongodb.com/manual/tutorial/query-documents/)

在`hello_mongodb.py`中，我新建了`xgm-database`数据库，并且插入了少量数据。  

我们可以在终端查看使用py操作的结果。打开终端，输入`mongo`，进入shell。使用`show dbs`查看所有的数据库，得到如下输出：  
```shell
> show dbs
admin          0.000GB
config         0.000GB
local          0.000GB
test_database  0.000GB
xgm-database   0.000GB
```

输入`use xgm-database`进入数据库，输入`show collections`查看数据库下都有什么collections（根据官网，collections相当于关系数据库中的“表”）
> A collection is a group of documents stored in MongoDB, and can be thought of as roughly the equivalent of a table in a relational database. 

得到  
```
> show collections
posts
profiles
```


最后使用`db.posts.find()`，即可查询到py文件插入的数据。   
```json
> db.posts.find()
{ "_id" : ObjectId("5c0e75bdfc10f1727a8d2e9e"), "author" : "Mike", "text" : "My first blog post!", "tags" : [ "mongodb", "python", "pymongo" ], "date" : ISODate("2018-12-10T14:18:37.697Z") }
{ "_id" : ObjectId("5c0e75bdfc10f1727a8d2e9f"), "author" : "Mike", "text" : "Another post!", "tags" : [ "bulk", "insert" ], "date" : ISODate("2018-11-12T11:14:00Z") }
{ "_id" : ObjectId("5c0e75bdfc10f1727a8d2ea0"), "author" : "Eliot", "title" : "MongoDB is fun", "text" : "and pretty easy too!", "date" : ISODate("2018-11-10T10:45:00Z") }
{ "_id" : ObjectId("5c0e7694fc10f172e9b5cedd"), "author" : "Mike", "text" : "My first blog post!", "tags" : [ "mongodb", "python", "pymongo" ], "date" : ISODate("2018-12-10T14:22:12.147Z") }
{ "_id" : ObjectId("5c0e7694fc10f172e9b5cede"), "author" : "Mike", "text" : "Another post!", "tags" : [ "bulk", "insert" ], "date" : ISODate("2018-11-12T11:14:00Z") }
{ "_id" : ObjectId("5c0e7694fc10f172e9b5cedf"), "author" : "Eliot", "title" : "MongoDB is fun", "text" : "and pretty easy too!", "date" : ISODate("2018-11-10T10:45:00Z") }
```

最后，我们可以使用`sudo service mongodb stop`退出mongo服务。


