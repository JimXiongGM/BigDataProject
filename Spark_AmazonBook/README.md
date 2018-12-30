# 使用Spark分析kaggle - Amazon sales数据

未完待续

## 目录 




## <p id=1>数据准备 

数据详情可见[公开数据说明文档](../Documentations/public_datas.md)。[点击这里](../Documentations/Hadoop_distribute.md)可以看到云端分布式配置详情。   

在说明文档中，Sample数据已经被上传到HDFS。



## hadoop streaming 获取salesrank时间范围

首先，编写mapper和reducer对数据进行描述性统计，获取每本书salesrank的最早和最迟时间。代码详见`mapper_kaggle_BeginEnd.py`。值得注意的是，这里几乎不用reducer，因为不需要对key进行统计，但是不上传reducer，hadoop streaming会报错，所以这里都上传。


本地测试一下：
```
root@master:~/HadoopStreamingPY3# cat 000721393X_com_norm.json | mapper_kaggle_BeginEnd.py | reducer_kaggle__BeginEnd.py
filename_test_568_first 2017-07-26_02:00:00,2018-06-30_08:00:00
```

提交到hadoop
```
hadoop jar /opt/hadoop-3.1.1/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar \
  -D mapreduce.job.name='KaggleAmazon_BeginEnd' \
  -input /Data_Sample/Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books/Sample_ranks_norm/*.json \
  -output /xgm/output/KaggleAmazon_BeginEnd01 \
  -mapper mapper_kaggle_BeginEnd.py \
  -reducer reducer_kaggle__BeginEnd.py \
  -file /root/HadoopStreamingPY3/mapper_kaggle_BeginEnd.py \
  -file /root/HadoopStreamingPY3/reducer_kaggle__BeginEnd.py

```


## spark join 

这里的操作直接在jupyter notebook上执行，相应代码和执行结果请看[这里](./PySpark-Kagggle-AmazonBook.ipynb)。

思路很简单，读取hadoop mapreduce 的结果为dataframe，和提供好的csv文件进行表连接即可。然后我们对`start-time`列升序和降序排列，看看这一列的极值。




## 年度排行榜统计



## 使用MongoDB存储



## 性能调优



## 错误调试

遇到No such file or directory，经过查询是windows系统下字符和ubuntu不兼容
```s
root@master:~/HadoopStreamingPY3# cat 000721393X_com_norm.json | mapper_kaggle_BeginEnd.py
-bash: ./mapper_kaggle_BeginEnd.py: /opt/anaconda3/bin/python^M: bad interpreter: No such file or directory
```

在vim下输入即可
```
:set ff=unix
```