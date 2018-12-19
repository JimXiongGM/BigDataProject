# 大数据存储与分析

## 前言  

本项目目标是基于阿里云搭建全分布式系统，运行Hadoop3+Spark+MongoDB+something else做一些好玩的事，目前正在构思与探索。这是笔者第一次上手大数据平台，因此秉持着”study with output“的精神，尝试把从下载软件到跑通代码的过程都记录下来，并且尽力”知其所以然“。所以本项目记录比较详细，适合新手阅读。

## 思路

本项目采用结构化+非结构化数据，初步采用Hadoop streaming进行数据处理，Pig分析结构化数据，使用MongoDB存储并分析非结构化数据。
 
## 目录  

因配置环境只需要一篇文档，这里把配置环境的说明文件直接放到Docs文件夹下。

### 环境安装
 
- [Hadoop3全分布式+Hadoop streaming环境搭建](./Documentations/Hadoop_distribute.md)  
- [MongoDB的本地安装](./Documentations/MongoDB_standalone.md)    
- [MongoDB的全分布式安装](./Documentations/MongoDB_distribute.md)    
- [Pig的全分布式安装](./Documentations/Pig_distribute.md) 
- 未完待续

### 数据集介绍

- [kaggle - Amazon sales rank data for print and kindle books](./Documentations/Kaggle_amazon-sales-rank-data-for-print-and-kindle-books.md)


### 项目
- [使用Hadoop Streaming分析kaggle数据](./HadoopStreaming_Kaggle/README.md)
- [使用全分布式Pig分析数据](./PigOnMap-Reduce/README.md)　　挖坑待填 
- [Python+MongoDB————爬取与存储数据](./MongDBWithCrawler/README.md)  
- [全分布下Hadoop和MongoDB的使用](./Documentations/Hadoop+MongoDB_Crawler.md)　　挖坑待填  
- 未完待续
