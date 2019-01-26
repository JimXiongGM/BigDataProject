# Hive HA模式搭建（未测试）

hive的HA模式，和hadoopHA有一些不同。hive只是一个客户端，数据库文件都存在hdfs中，因此hive的HA更像是一种均衡负载。

## 启动

这里尝试在master和slave2做负载均衡。先把hive给slave2。在master端
```
scp -r /opt/hive-3.1.1 root@slave2:/opt/
```

接着从本项目下拷贝hive-site.xml到master。hive-site.xml需要修改的部分已经列在文件最前面。在本地端
```
scp ./Documentations/Hive_config_files/conf-HA/hive-site.xml root@master:/opt/hive-3.1.1/conf/;
scp ./Documentations/Hive_config_files/conf-HA/hive-site.xml root@slave2:/opt/hive-3.1.1/conf/;
```

在slave2端配置环境变量
```
echo '
# HIVE SETTINGS
export HIVE_HOME=/opt/hive-3.1.1
export PATH=$HIVE_HOME/bin:$PATH
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib:$HIVE_HOME/lib
' >> /etc/bash.bashrc ;
source /etc/bash.bashrc;
```

使用如下任一命令开启hiveserver2
```
$HIVE_HOME/bin/hiveserver2
or
nohup hive --service hiveserver2 &
```

进入zookeeper可以看到集群已经开启
```
/opt/zookeeper-3.4.13/bin/zkCli.sh
ls /
```

查看端口是否已经被监听
```
netstat | grep 10001
```

## beeline

Beeline是Hive新的命令行客户端工具。

```
$HIVE_HOME/bin/beeline

beeline -u "jdbc:hive2://master:2181,slave1:2181,slave2:2181,slave3:2181/default;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2_zk" -nhive -phive$
```


## 测试

未完待续

