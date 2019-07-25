# 大数据存储与分析

大数据生态链初探。
 
## 目录  

因配置环境只需要一篇文档，这里把配置环境的说明统一文件放到`Documentations`文件夹下。

## 环境安装与Hello-World DEMO
 
0. [阿里云虚拟机集群设置](./Documentations/Aliyun_4ECS.md)

### 核心环境搭建
1. [Hadoop3全分布式 + Hadoop streaming环境搭建](./Documentations/Hadoop_distribute.md)---依赖[0]
2. [Hadoop3分布式HA模式搭建](./Documentations/Hadoop_distribute_HA.md)---依赖[1]

3. [Spark全分布式安装](./Documentations/Spark_distribute.md)---依赖[1]
4. [Spark分布式HA模式搭建](./Documentations/Spark_distribute_HA.md)---依赖[3]

### spark探索

本节均依赖[3]或[4]。

5. [Scala语法基础（无demo）](./Documentations/ScalaBasic.md)
6. [Scala + Spark基础（scala+sbt+spark hello world）](./Documentations/ScalaSpark.md)
7. [Scala + Spark Streaming基础（scala+sbt+SparkStreaming hello world）](./Documentations/SparkStreaming_Scala.md)
8. [Spark + SQL实例 (Scala + python3)](./Documentations/SparkSQLDEMO_Scala.md)
9. [Jupyter Notebook + Spark 配置](./Documentations/JupyterNotebook.md)

### 生态环境搭建

### MySQL搭建

10. [MySQL 8.0环境搭建](./Documentations/MySql_8.0.md)

#### Hive与HBASE
11. [HBASE分布式环境搭建](./Documentations/Hbase_distribute.md)
12. [Hive环境搭建](./Documentations/Hive_distribute.md)
13. [Hive HA模式搭建（未测试）](./Documentations/Hive_distribute_HA.md)

#### MongoDB与Pig
14. [MongoDB的本地安装 + PyMongo的基本操作](./Documentations/MongoDB_standalone.md)
15. [MongoDB的全分布式安装](./Documentations/MongoDB_distribute.md)
16. [Pig的全分布式安装](./Documentations/Pig_distribute.md)


## 数据集介绍

### 公开数据集

这一部分数据集能够在公开渠道下载。  

- [kaggle - Amazon sales rank data for print and kindle books--3.66GB](./Documentations/public_datas.md)
- [THUCNews数据集--2.04GB](./Documentations/public_datas.md)
- [全网新闻数据(SogouCA,2012)数据集--2.08GB](./Documentations/public_datas.md)
- [高频交易数据(tick_csv_daily)--7.16GB](./Documentations/public_datas.md)


### 爬虫数据集

这一部分数据集由笔者自行爬取获得。

- [LandChina数据集--14.5GB](./Documentations/private_datas.md)
- [财新网新闻文本数据集--42MB](./Documentations/private_datas.md)


## 上手

- [使用Spark分析kaggle - Amazon sales数据](./Spark_AmazonBook/README.md)
- [PySpark初探](./Spark_learningPySpark/README.md)
- [Python+MongoDB————爬取与存储数据](./MongDBWithCrawler/README.md)
- [使用全分布式Pig分析数据](./PigOnMap-Reduce/README.md)
- [全分布下Hadoop和MongoDB的使用](./Documentations/Hadoop+MongoDB_Crawler.md)


## 备忘

- [新装ubuntu设置备忘](./Documentations/NewUbuntu18.md)