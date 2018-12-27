# 使用Spark分析LandChina数据

## 目录 




## <p id=1>数据准备 

这里使用的是LandChina数据，详情可见[说明文档](../Documentations/private_datas.md)。[点击这里](../Documentations/Hadoop_distribute.md)可以看到云端分布式配置详情。   

在说明文档中，数据已经被上传到HDFS。

首先构思想要什么。由于笔者之前已经把各种html网页提取成了规范的csv，所以现在我们有半结构化的html源码和结构化的csv文件。学习spark从简单开始，这里先使用csv文件进行分析处理。

## Spark基本操作



