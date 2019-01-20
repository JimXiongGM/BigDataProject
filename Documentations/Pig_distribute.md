# Pig的分布式安装

为什么要用Pig？因为
- Pig的语法结构类似SQL，轻量、易懂、开发高效
- Pig适合在HDFS中处理结构化数据
- Pig能够内嵌Python
- And so on

下面在之前搭建好的全分布式云端上搭建Pig。这里的云端配置在之前的文档中可以找到：[Hadoop3的全分布式安装回忆](./Documentations/Hadoop_distribute.md)  

值得注意的是，Pig作为客户端程序运行，即使你准备在Hadoop集群上使用Pig，你也不需要在集群上做任何安装。Pig从本地提交作业，并和Hadoop进行交互。

## 下载并解压Pig

从[官网](http://pig.apache.org/releases.html)下载，`wget https://mirrors.tuna.tsinghua.edu.cn/apache/pig/latest/pig-0.17.0.tar.gz`，并解压，`tar -zxvf pig-0.17.0.tar.gz -C /opt/`，重命名，`mv /opt/pig-0.17.0 /opt/pig`  

## 添加环境变量

执行`echo 'export PIG_INSTALL=/opt/pig' >> /etc/bash.bashrc`，`echo 'export PATH=$PATH:$PIG_INSTALL/bin' >> /etc/bash.bashrc`，`source /etc/bash.bashrc`即可

## 运行

根据[官方文档](http://pig.apache.org/docs/r0.17.0/start.html)，Pig可以以6种方式启动。这里我们以`Local Mode`和`Mapreduce Mode`测试启动  

### 运行local mode

使用`pig -x local`即可启动shell，显示为`grunt> `。输入`quit`退出。

### 运行Mapreduce Mode

这里先确保hadoop处于打开状态，确保Hadoop的环境变量有正确设置。可以使用`echo $HADOOP_HOME`查看。

根据官网，pig命令默认以Mapreduce方式启动，因此直接输入`pig`
> Mapreduce mode is the default mode  

可以看到输出
```s
2018-12-13 19:44:38,146 [main] INFO  org.apache.pig.backend.hadoop.executionengine.HExecutionEngine - Connecting to hadoop file system at: hdfs://master.local:9000
```

简单测试一下是否能够读取HDFS的数据，使用`ls /`，可以看到：
```s
grunt> ls /
hdfs://master.local:9000/tmp	<dir>
hdfs://master.local:9000/xgm	<dir>
```

环境搭建成功，so easy。