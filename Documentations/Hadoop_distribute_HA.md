# Hadoop3分布式HA模式搭建

HA模式即高可用模式，这个模式之下namenode挂掉没事，备用节点可以顶上。但是该模式安装比较麻烦，需要安装zookeeper作为集群调度器判断namenode是否离线，还要配置journalnode进行日志转存操作等等。

这里参考的资料主要来源于杨曦所著的[HBASE不睡觉书](https://read.douban.com/ebook/51046818/)，这本书口语化的表达非常适合初学者阅读，是一本入门佳作。

## 目录

- [zookeeper安装](#1)
- [hadoop HA 模式配置](#2)


## <p id=1>zookeeper安装

### 下载解压

首先下载解压并赋权。
```
cd ~/xiazai;
wget http://ftp.cuhk.edu.hk/pub/packages/apache.org/zookeeper/zookeeper-3.4.13/zookeeper-3.4.13.tar.gz;
tar -zxvf zookeeper-3.4.13.tar.gz;
mv zookeeper-3.4.13 /opt/;
chown -R root.root /opt/zookeeper-3.4.13;
```

### 设置集群配置文件

需要配置5处，分别是环境变量、zoo.cfg、myid、zkEnv.sh，建立目录并设置权限，直接copy即可。

```
echo '配置环境变量';
echo 'export ZOOKEEPER_HOME=/opt/zookeeper-3.4.13' >> /etc/bash.bashrc;
source /etc/bash.bashrc;

echo '设置zoo.cfg';
rm -f /opt/zookeeper-3.4.13/conf/zoo.cfg;
touch /opt/zookeeper-3.4.13/conf/zoo.cfg;
echo 'tickTime=2000
initLimit=10
syncLimit=5
dataDir=/data/zookeeper
clientPort=2181
server.255=master:2888:3888
server.1=slave1:2888:3888
server.2=slave2:2888:3888
server.3=slave3:2888:3888' >> zoo.cfg;

echo '设置master的myid'
touch /data/zookeeper/myid;
echo '255' >> /data/zookeeper/myid;

echo '设置zkEnv.sh'
cd  /opt/zookeeper-3.4.13/bin;
sed -i '26i ZOO_LOG_DIR=/data/logs/zookeeper' zkEnv.sh;

echo '设置权限'
mkdir -p /data/zookeeper;
chown root.root /data/zookeeper;
mkdir-p /data/logs/zookeeper;
chown root.root /data/logs/zookeeper;
```
### 分发与启动

这里只要直接把刚刚配置好的文件夹整个复制到集群即可。

```
scp -r /opt/zookeeper-3.4.13 root@slave1:/opt;
scp -r /opt/zookeeper-3.4.13 root@slave2:/opt;
scp -r /opt/zookeeper-3.4.13 root@slave3:/opt;
ls
```

复制完文件之后需要分别进入每节点建立目录和myid文件，命令如下。

`ssh root@slave1`
```
mkdir -p /data/zookeeper;
chown root.root /data/zookeeper;
touch /data/zookeeper/myid;
echo '1' >> /data/zookeeper/myid;

echo 'export ZOOKEEPER_HOME=/opt/zookeeper-3.4.13' >> /etc/bash.bashrc;
source /etc/bash.bashrc;

rm -rf /data/logs/zookeepers/*;
rm -rf /data/zookeepers/*;
$ZOOKEEPER_HOME/bin/zkServer.sh start

exit
```

`ssh root@slave2`
```
mkdir -p /data/zookeeper;
chown root.root /data/zookeeper;
touch /data/zookeeper/myid;
echo '2' >> /data/zookeeper/myid;

echo 'export ZOOKEEPER_HOME=/opt/zookeeper-3.4.13' >> /etc/bash.bashrc;
source /etc/bash.bashrc;

rm -rf /data/logs/zookeepers/*;
rm -rf /data/zookeepers/*;
$ZOOKEEPER_HOME/bin/zkServer.sh start

exit
```

`ssh root@slave3`
```
mkdir -p /data/zookeeper;
chown root.root /data/zookeeper;
touch /data/zookeeper/myid;
echo '3' >> /data/zookeeper/myid;

echo 'export ZOOKEEPER_HOME=/opt/zookeeper-3.4.13' >>/etc/bash.bashrc;
source /etc/bash.bashrc;

rm -rf /data/logs/zookeepers/*;
rm -rf /data/zookeepers/*;
$ZOOKEEPER_HOME/bin/zkServer.sh start

exit
```

### master启动

配置完毕之后直接启动即可。根据教材的说法，最好清理下log文件，避免启动失败。

```
rm -rf /data/logs/zookeepers/*;
rm -rf /data/zookeepers/*;
$ZOOKEEPER_HOME/bin/zkServer.sh start
```

### 测试zookeeper

通过如下命令能够显示zookeeper是否启动成功，如果成功，bash的输出中能看到mode

```
$ZOOKEEPER_HOME/bin/zkServer.sh status
```

```bash
root@master:~# $ZOOKEEPER_HOME/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper-3.4.13/bin/../conf/zoo.cfg
Mode: leader
```

### 查看日志

启动失败是很正常的，通过如下命令能够查看日志
```
cat /data/logs/zookeeper/zookeeper.out
```

### 停止
```
$ZOOKEEPER_HOME/bin/zkServer.sh stop
```

## <p id=2>hadoop HA 模式配置

### 更新配置

这里不同于之前的非HA模式，改变了文件路径，不变也没事。
```
mkdir -p /data/hadoop/hdfs/namenode;
mkdir -p /data/hadoop/hdfs/datanode;
chown -R root.root /data/hadoop;
```

### 拷贝文件

比较快的方法是直接clone本项目，进入本项目根目录执行以下命令，把`./Documentations/Hadoop3_config_files`整个文件夹拷到云端。
```
scp -r ./Documentations/Hadoop3_config_files root@playbigdata.top:/root/;
```

在master端，我们可以直接把`etc-HA`中的配置文件拷贝到相应的位置，完成安装。

```
cp -f /root/Hadoop3_config_files/etc-HA/* /opt/hadoop-3.1.1/etc/hadoop/;
scp /root/Hadoop3_config_files/etc-HA/* root@slave1:/opt/hadoop-3.1.1/etc/hadoop/;
scp /root/Hadoop3_config_files/etc-HA/* root@slave2:/opt/hadoop-3.1.1/etc/hadoop/;
scp /root/Hadoop3_config_files/etc-HA/* root@slave3:/opt/hadoop-3.1.1/etc/hadoop/;

cp -f /root/Hadoop3_config_files/sbin-HA/* /opt/hadoop-3.1.1/sbin/;
scp /root/Hadoop3_config_files/sbin-HA/* root@slave1:/opt/hadoop-3.1.1/sbin/;
scp /root/Hadoop3_config_files/sbin-HA/* root@slave2:/opt/hadoop-3.1.1/sbin/;
scp /root/Hadoop3_config_files/sbin-HA/* root@slave3:/opt/hadoop-3.1.1/sbin/;


```

### 启动journalnode

在4台机器上使用如下命令，即4台机器都作为journalnode
```
mkdir -p /data/hadoop/hdfs/jn;
chown root:root /data/hadoop/hdfs/jn;
hdfs --daemon start journalnode;
exit
```

### 启动namenode

这里的启动命令比较麻烦，而且顺序不能变。在master和slave1上执行
```
hdfs namenode -format;
hdfs namenode -bootstrapStandby;
```
只在master上执行
```
hdfs namenode -initializeSharedEdits;
```
在master和slave1上执行
```
hdfs --daemon start namenode; 
```


### 配置自动failover

自动failover说的是使多个namenode中的一个为active，其余为备用状态。

上文中我们已经启动了zookeeper，这里需要保持zookeeper集群启动。

进入master和slave1，使用`hdfs --daemon stop namenode`停止namenode，然后启动zkfc
```
hdfs zkfc -formatZK;
hdfs --daemon start zkfc;
start-dfs.sh;
```

如果一切顺利，输出如下
```bash
root@master:~# jps
11296 NameNode
8932 JournalNode
8679 QuorumPeerMain
13256 Jps
12426 DFSZKFailoverController
```
打开网址`http://master:50070`，页面如下
![png](./imgs/hadoop-ha-50070.png)


### 停止journalnode

hdfs --daemon stop journalnode

