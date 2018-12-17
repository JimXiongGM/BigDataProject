# Hadoop3全分布式+Hadoop Streaming环境搭建 

可以说是站在巨人的肩膀上[@daviddwlee84](https://github.com/daviddwlee84)，我才能较快地搭建好全分布式Hadoop。这位同学的主要贡献是利用Python中的fabric包，实现了一键自动安装Hadoop3.1.1，不过他的环境是4块树莓派3b+，并基于本地局域网。[链接](https://github.com/daviddwlee84/RaspPi-Cluster)在此。  

上述工具可以为我们实现批量测试、批量执行等基本操作，但是为了熟悉Hadoop的安装流程，为了能够在出问题的时候找到出错的原因，这里对Hadoop的安装细节进行梳理。我们可以从网络上找到大把的Hadoop3安装步骤，这里推荐读者先自行搜索、熟悉安装流程和Hadoop文件结构，再阅读本章节。  

## 目录

> - [配置服务器的host/hostname](#1)  
> - [开放阿里云的端口](#2)  
> - [配置服务器之间免密钥登陆](#3)  
> - [下载解压Hadoop3.1.1](#4)  
> - [配置Hadoop](#5)  
> - [使用Hadoop Streaming+Python3](#6)   
> - [错误分析以及调试](#7)  
> - [鸣谢](#8)


## <p id="1">配置服务器的host/hostname

将master节点的hosts设置为如下，使用`vim /etc/hosts`编辑。并且**一定**要注释localhost这一行。
```
内网ip master  
对应公网ip slave1  
对应公网ip slave2  
对应公网ip slave3  
对应公网ip slave4
```
同时使用`vim /etc/hostname`将本机的hostname设置为
```
master
```
接下来逐一进入slave节点，使用`vim /etc/hosts`编辑。同样**一定**要注释localhost这一行，这里的master改成公网ip。
```
对应公网ip master  
对应公网ip slave1  
对应公网ip slave2  
对应公网ip slave3  
对应公网ip slave4
```
同时使用`vim /etc/hostname`设置对应的hostname，即slave1~4
```
slave1
```
重启所有的节点即可。

## <p id="2">开放阿里云的端口

**非常重要**的一点，阿里云默认只开放22，8080等几个端口，这显然是不行的。我们需要登陆所有机器的阿里云控制台，手动修改端口访问权限。我这里非常不安全地开放了所有的端口。具体操作非常简单，登陆网页版后台，点击左侧防火墙，设置端口为1/65535，如下图所示。  

![avatar](./aliyun_port.png)


## <p id="3">配置服务器之间免密钥登陆

这一块非常重要，Hadoop之间需要进行免密通讯，且云服务器之间也频繁需要ssh操作。具体操作网络上很多，这里不展开。在master节点使用`ssh root@slave1`进行测试，如果能够免密登陆成功，即配置完成。  

## <p id="4">下载解压Hadoop3.1.1

下载`hadoop-3.1.1-src.tar.gz`到每一个节点，并且所有节点都解压到同一路径：`/opt/hadoop3.1.1`

## <p id="5">配置Hadoop

ubuntu系统的源码运行模式就像windows的绿色文件运行模式，只要解压即可用，非常方便。这里对Hadoop配置文件进行设置。这一块的内容需要非常小心，网络上存在大量的教程，但是环境不同，需要配置的文件也不一样，我们需要确切知道每一个配置文件的内容以及参数含义，出错的时候才能找到解法。  

本文中所有文件都可以在当前目录下的`Hadoop3_config_files`文件夹找到，这里对配置文件进行总结。

### 配置hadoop3.1.1/etc/hadoop下文件

非常重要，这里一共要配置8个文件。

#### 1.core-site.xml

配置HDFS的访问路径和端口，这里的设置可以照搬网络。

#### 2.hdfs-site.xml

配置HDFS的副本数、datanode与namenode的文件存储路径，这里的设置可以照搬网络。本文为了加快调试速度，将HDFS副本数设置为1.

#### 3.master

就一行，为了声明master的ip，对应关系已经在hosts文件中声明。这里的设置可以照搬网络。

#### 4.slaves

3行，为了声明slaves的ip，对应关系已经在hosts文件中声明。这里的设置可以照搬网络。这是Hadoop2.X的用法，为了安全，这里也配置。

#### 5.workers

3行，为了声明slaves的ip，对应关系已经在hosts文件中声明。这里的设置可以照搬网络。这是新用法。

#### 6.yarn-site.xml

配置yarn的调度机制，不能照搬网络！关于该文件的详细配置可以自行搜索，[官网文档](https://hadoop.apache.org/docs/r3.1.1/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)在这里。本文展示几个关键配置。

1).vcores设置。非常重要的设置，本文使用的是阿里云的学生机，只有1核1线程，所以这里只能设置为1.
```js
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>1</value>
    </property>
```
我们可以使用`lscpu`查看cpu的核心数、线程数，这里可以设置的最大值是核心*线程数。  

2).最小/最大分配核心设置。最大分配核心是关键，这里的设置不能超过单个节点的核心*线程数。这里都是1...
```js
    <property>
        <name>yarn.scheduler.minimum-allocation-vcores</name>
        <value>1</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-vcores</name>
        <value>1</value>
    </property>
```

3).yarn内存分配设置。学生机的内存为2G，因此这里设置如下。
```js
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>1024</value> <!-- max 75% of memory for Node (2GB) -->
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>1024</value>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>64</value>
    </property>
```

4).配置yarn address。遇到奇怪的错误之后总结的经验...
```js
     <property>
         <name>yarn.resourcemanager.address</name>
         <value>master:8032</value>

     </property>
```

#### 7.mapred-site.xml

mapper-reduce相关配置，不能照搬网络！  

1).配置内存，同样根据机器配置进行设置
```js
    <property>
        <name>yarn.app.mapreduce.am.resource.mb</name>
        <value>512</value>
    </property>
    <!-- How much memory will be allocated to each map or reduce operation.
    This should be less than the maximum size. -->
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>256</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>256</value>
    </property>
```

#### 8.capacity-scheduler.xml

scheduler相关配置，需要微调。  

1).scheduler最大可以使用的资源量。各种出错之后设置的经验值。
```js
  <property>
    <name>yarn.scheduler.capacity.maximum-am-resource-percent</name>
    <value>0.3</value>
    <description>
      Maximum percent of resources in the cluster which can be used to run
      application masters i.e. controls number of concurrent running
      applications.
    </description>
  </property>
```

### 配置环境变量

这一块比较简单，我们可以直接照搬网络。使用`vim /etc/bash.bashrc`，在每一台节点上添加如下信息，并使用`source /etc/bash.bashrc`使之生效
```js
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
export HADOOP_HOME=/opt/hadoop-3.1.1
export HADOOP_INSTALL=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native


export HADOOP_LIBEXEC_DIR=$HADOOP_HOME/libexec
export JAVA_LIBRARY_PATH=$HADOOP_HOME/lib/native:$JAVA_LIBRARY_PATH
export PATH=.:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
```

不出意外，到这里已经配置完毕，可以启动Hadoop。

##启动

启动之前，我们先进行format操作和授权操作。  

在master节点，使用`hdfs namenode -format`，初始化hdfs相关配置。此时，根据上文`hdfs-site.xml`的配置：
```js
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///hadoop/namenode</value>
    </property>
```
我们会在本地文件目录下找到`/hadoop/namenode`文件，同样，在datanode节点，我们能找到`/hadoop/datanode`文件夹。这里我们对所有节点的该文件夹进行授权操作。在每一节点上执行`chmod -R 777 /hadoop`命令，即可对该文件夹以及子文件夹授予777权限。我们可以通过`ls -ld /hadoop`命令查看指定文件夹的权限设置情况，显示为`drwxrwxrwx`说明该文件夹对所有用户都有写入权限。  

在master节点，使用`start-all.sh`启动Hadoop。当然也可以使用`start-dfs.sh`以及`start-yarn.sh`启动。启动成功之后，输入`jps`，可以看到如下。
```s
root@master:~# jps
30000 Jps
24849 ResourceManager
889 Application
24620 SecondaryNameNode
24365 NameNode
```
此时通过浏览器访问`http://master:8088`可以看到Hadoop节点界面，访问`http://master:50070`可以看到HDFS使用情况。


## <p id="6">使用Hadoop Streaming + Python3 

为了测试Hadoop确实搭建成功，本文使用Hadoop Streaming运行Python版的mapper和reducer。  

关于Hadoop Streaming是什么，以及如何工作，请读者自行查阅网络资料，[这里](http://hadoop.apache.org/docs/current/hadoop-Streaming/HadoopStreaming.html)是官网。简要地说，这是把Hadoop的输入统一为stdin，输出统一为stdout。这样可以使用任何编程语言进行流式处理。这里使用Python3进行处理。

### 配置python3环境

ubuntu16自带Python2.7以及Python3.5，这里需要切换默认的Python版本为Python3。很简单只需要两条命令
```s
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150
```
最后的100和150表示优先级。如果要切换到Python2，执行`sudo update-alternatives --config python`，按照提示输入选择数字并回车即可。  

使用命令`python --version`确认当前版本号，使用命令`which python`确认路径为`/usr/bin/python`。


### 范例 WordCount

WordCount是官网提供的统计词频的范例程序，这里的py程序源码和数据文本可以在`Documentations\WordCountDemo`文件夹下找到。

### 本地测试WordCount

把文件放到自己的路径。  

Hadoop Streaming采用标准输入输出流，因此可以本地测试，通过之后再提交。使用`echo "foo foo quux labs foo bar quux" | /root/xgm/mapper_WordCount.py `命令测试`mapper_WordCount.py`文件，得到的输出如下
```s
root@master:~# echo "foo foo quux labs foo bar quux" | /root/xgm/mapper_WordCount.py
foo     1
foo     1
quux    1
labs    1
foo     1
bar     1
quux    1
```

使用`echo "foo foo quux labs foo bar quux" | /root/xgm/mapper_WordCount.py | sort -k1,1 | /root/xgm/reducer_WordCount.py`测试两个文件，得到的输出如下
```s
root@master:~# echo "foo foo quux labs foo bar quux" | /root/xgm/mapper_WordCount.py | sort -k1,1 | /root/xgm/reducer_WordCount.py
bar     1
foo     3
labs    1
quux    2
```

测试通过。

### 上传文本到HDFS

将目录下的文本上传到hdfs
```s
hdfs dfs -mkdir -p /xgm/input;
hdfs dfs -copyFromLocal /root/xgm/test.txt /xgm/input/
```

### 提交WordCount

在master端，使用`find / -name hadoop-streaming*`命令找到相应jar文件，这里的结果是`/opt/hadoop-3.1.1/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar`    

直接使用如下命令，即可
```s
hadoop jar /opt/hadoop-3.1.1/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar \
  -D mapreduce.job.name='WordCount01' \
  -input /xgm/input/test.txt \
  -output /xgm/output/WordCount01 \
  -mapper mapper_WordCount.py \
  -reducer reducer_WordCount.py \
  -file /root/xgm/mapper_WordCount.py \
  -file /root/xgm/reducer_WordCount.py
```

**特别注意**，Hadoop规定，输出文件夹不能存在，所以这里的` -output /xgm/output/WordCount01`一定要保证不存在`WordCount01`文件夹。  

我们可以使用浏览器打开`http://master:8088`，查看相应任务。实测，在5个阿里云学生机节点的情况下，20秒跑完。

### 查看输出

我们可以点击`http://master:50070`右上角的`Utilities`下拉菜单中的`Browse the file system`查看hdfs文件。这里可以看到`/xgm/output/WordCount09`目录下有两个文件，分别是`_SUCCESS`和`part-00000`。  

同样可以在master端使用命令` hdfs dfs -cat /xgm/output/WordCount09/part-00000`查看，输出为
```
...
...
with?"  1
within  4
without 19
won     1
won't   1
wood    1
wood.   1
wooden  6
word    6
word,   1
words,  1
words.  1
wore    1
work    60
work,   9
...
...
```


## <p id="7">错误分析以及调试

不算搭建环境，笔者跑通Hadoop Streaming用了3天时间，期间各种报错是非常正常的。这里给读者们整理一下分析错误的常用手段。  

### 查看logs下的日志

Hadoop master节点会启动ResourceManager，NameNode、SecondaryNameNode服务，相应的日志文件存放在`$HADOOP_HOME/logs`文件夹下。如果遇到网页UI打不开、NameNode无法启动的情况，可以使用命令` `以及命令` `查看相应日志。如果遇到提交任务的问题，例如Applications FAILED、Applications 一直 RUNNING 等情况，可以通过命令` `查看日志文件。  

我们可以使用vim查找`ERROR`，`WARN`，相应Application_ID等关键字，查找日志内容并分析错误。

### 查看yarn job的日志

笔者遇到了Applications RUNNING不停的情况，后来经过查询是ResourceManager虚拟cpu、内存设置不当导致。这里可以使用`yarn logs -applicationId application_1544978267369_0001 > temp2.log`命令，将特定application_ID的运行日志导出为文件，并进行错误分析。

### py文件本地调试

关于mapper和reducer的py文件本地调试，这里要**特别注意**两点。  

- 1.文件首行声明编译器路径  

在代码首行应加上`#!/usr/bin/python`。  


- 2.Python代码缩进不能使用tab  

如果使用诸如pycharm、VScode等IDE编写Python程序，我们很容易使用tab键进行代码缩进，但是这在ubuntu直接执行可能会出问题，需要将一个tab键替换为4个空格。这里可以手动将tab替换为4个空格，也可以使用`sudo vim /etc/vim/vimrc`，在最后加入以下即可
```s
set ts=4
set expandtab
set autoindent
```

## <p id="8">鸣谢

特别感谢[@daviddwlee84](https://github.com/daviddwlee84)和[@wilsonwz94](https://github.com/wilsonwz94)的帮助，没有你们的帮助，我的进度将放慢10倍。


