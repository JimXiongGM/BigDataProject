# 大数据存储与分析

## 前言  

本项目目标是基于阿里云搭建全分布式系统，运行Hadoop3+Spark2+MongoDB+something else做一些好玩的事，目前正在构思与探索。这是笔者第一次上手大数据平台，因此秉持着“study with output”的精神，尝试把从下载软件到跑通代码的过程都记录下来，并且尽力“知其所以然”。所以本项目记录比较详细，适合新手阅读。

## 思路

边学边记。
 
## 目录  

因配置环境只需要一篇文档，这里把配置环境的说明统一文件放到`Documentations`文件夹下。

## 环境安装与Hello-World DEMO
 
- [Hadoop3全分布式 + Hadoop streaming环境搭建](./Documentations/Hadoop_distribute.md)
- [Spark全分布式安装](./Documentations/Spark_distribute.md)
- [Scala语法基础](./Documentations/ScalaBasic.md)
- [Scala + Spark基础](./Documentations/ScalaSpark.md)
- [Spark Streaming基础 + 实例 (Scala)](./Documentations/SparkStreaming_Scala.md)
- [Spark + SQL实例 (Scala + python3)](./Documentations/SparkSQLDEMO_Scala.md)
- [Jupyter Notebook + Spark 配置](./Documentations/JupyterNotebook.md)
- [MongoDB的本地安装 + PyMongo的基本操作](./Documentations/MongoDB_standalone.md)
- [MongoDB的全分布式安装](./Documentations/MongoDB_distribute.md)
- [Pig的全分布式安装](./Documentations/Pig_distribute.md)
- 未完待续

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
- [使用Hadoop Streaming分析kaggle - Amazon sales数据](./HadoopStreaming_Kaggle/README.md)
- [Python+MongoDB————爬取与存储数据](./MongDBWithCrawler/README.md)
- [使用Spark分析kaggle - Amazon sales数据](./Spark_AmazonBook/README.md)
- [使用全分布式Pig分析数据](./PigOnMap-Reduce/README.md)　　挖坑待填
- [全分布下Hadoop和MongoDB的使用](./Documentations/Hadoop+MongoDB_Crawler.md)　　挖坑待填
- 未完待续
