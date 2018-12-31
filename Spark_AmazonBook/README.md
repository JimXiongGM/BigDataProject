# 使用Spark分析kaggle - Amazon sales数据

本文使用hadoop streaming + pyspark对Amazon book salesrank进行了简单的统计分析，首先按照月度统计salesrank均值，接着给出了2018年6月的排行统计。

## 目录 

- [数据准备](#1)
- [hadoop streaming 获取salesrank时间范围](#2)
- [spark join](#3)
- [月度排行榜统计--Hadoop streaming](#4)
- [月度排行榜统计--pyspark](#5)
- [性能调优](#6)
- [错误与调试](#7)


## <p id=1>数据准备 

数据详情可见[公开数据说明文档](../Documentations/public_datas.md)。[点击这里](../Documentations/Hadoop_distribute.md)可以看到云端分布式配置详情。   

在说明文档中，Sample数据已经被上传到HDFS，且本文数据基于sample，完整数据集测试日后补充。



## <p id=2>hadoop streaming 获取salesrank时间范围

首先，编写mapper和reducer对数据进行描述性统计，获取每本书salesrank的最早和最迟时间。代码详见`mapper_kaggle_BeginEnd.py`。值得注意的是，这里几乎不用reducer，因为不需要对key进行统计，但是不上传reducer，hadoop streaming会报错，所以这里都上传。


本地测试一下：
```
root@master:~/HadoopStreamingPY3# cat 000721393X_com_norm.json | mapper_kaggle_BeginEnd.py | reducer_kaggle__BeginEnd.py
filename_test_568_first 2017-07-26_02:00:00,2018-06-30_08:00:00
```
这里有遇到'broken pipe'问题，详见本文[错误与调试](#)。

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


## <p id=3>spark join 

这里的操作直接在jupyter notebook上执行，相应代码和执行结果请看[这里（jupyter nobook格式）](./PySpark-Kaggle-AmazonBook.ipynb)，如果因为排版问题，这里同时提供了[markdown版本](./PySpark-Kaggle-AmazonBook.md)

思路很简单，读取hadoop mapreduce 的结果为dataframe，和源文件提供csv文件进行表连接即可。然后我们对`start-time`列升序和降序排列，看看这一列的极值。



## <p id=4>月度排行榜统计--Hadoop streaming

从上述的代码执行结果，我们能看出kaggle的这份数据极差较大，做年度统计意义有限，但是做月度分析还是有意义的。这里我们继续使用hadoop streaming，对数据集的月度情况做一个统计。

思路是把数据从2017年1月1日到2018年6月30日按照时间切片，分为18个自然月，进行月度salesrank均值统计。首先需要知道每一个月份对应的时间戳值：

时间点 | 时间戳
--- | ---
2017年1月1日 | 1483200000
2017年2月1日 | 1485878400
2017年3月1日 | 1488297600
2017年4月1日 | 1490976000
2017年5月1日 | 1493568000
2017年6月1日 | 1496246400
2017年7月1日 | 1498838400
2017年8月1日 | 1501516800
2017年9月1日 | 1504195200
2017年10月1日 | 1506787200
2017年11月1日 | 1509465600
2017年12月1日 | 1512057600
2018年1月1日 | 1514736000
2018年2月1日 | 1517414400
2018年3月1日 | 1519833600
2018年4月1日 | 1522512000
2018年5月1日 | 1525104000
2018年6月1日 | 1527782400
2018年7月1日 | 1530374400

### mapper


思路是对每个key值做判断，看看属于哪一个区间，将值填入对应的卡槽（slot）。这一部分笔者为原创，简介如下。每一个mapper输出键为文件名，即ASIN，键为一个list，共18个slot，对于每一个key，判断其属于哪一个slot，填入并print。这样每一个json文件将会print上千个如下的key-value，每一个key-value只有一个slot有值，其余为0。详情见[mapper_18months.py](./mapper_18months.py)

<"filenam" \t "[value0][value1].....[value17]">


### reducer

思路是对相同key的key-value进行分slot统计，即对于相同key，有一个累加器list和一个求和list，遇到相应slot非零，则累加器list+=1.求和list+=相应值。最后相应slot相除并输出。详情见[reducer_18months.py](./reducer_18months.py)
```
ing_slot_accumlators = [0,0,......,0]　　#共18个
ing_slot_sums = [0,0,......,0]　　#共18个
```

### 测试与提交

将mapper和reducer上传到云端，同样注意broken pipe问题。使用如下命令测试

```
root@master:~/HadoopStreaming_Month# cat 000721393X_com_norm.json  |  mapper_18months.py | sort -t ' ' -k 1 | reducer_18months.py
filename_test_970       0       0       0       0       0       0       542483  836820  745066  453745  450170  714322  687373  956912  746508  683338  814608  548967
```
**特别注意**：把mapper文件中的`本地测试filename`注释掉，启用hadoop环境变量！

提交到hadoop集群：
```
hadoop jar /opt/hadoop-3.1.1/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar \
  -D mapreduce.job.name='KaggleAmazon_18months' \
  -input /Data_Sample/Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books/Sample_ranks_norm/*.json \
  -output /xgm/output/KaggleAmazon_18months02 \
  -mapper mapper_18months.py \
  -reducer reducer_18months.py \
  -file /root/HadoopStreaming_Month/mapper_18months.py \
  -file /root/HadoopStreaming_Month/reducer_18months.py
```


## <p id=5>月度排行榜统计--pyspark

查看本目录下的`PySpark-Kagggle-AmazonBook_Sample_18months`文件即可看到源码和输出，这里同样提供了[jupyter版本](./PySpark-Kagggle-AmazonBook_Sample_18months.ipynb)和[markdown版本](PySpark-Kagggle-AmazonBook_Sample_18months.md)，点击可以查看。


## <p id=6>性能调优

未完待续


## <p id=7>错误与调试

### 字符不兼容

遇到No such file or directory与broken pipline，经过查询是windows系统下字符和ubuntu不兼容
```s
root@master:~/HadoopStreamingPY3# cat 000721393X_com_norm.json | mapper_kaggle_BeginEnd.py
-bash: ./mapper_kaggle_BeginEnd.py: /opt/anaconda3/bin/python^M: bad interpreter: No such file or directory
```

在vim下输入即可
```
:set ff=unix
```

### 权限不足

遇到permission denied问题，使用如下命令
```
chmod -R 777 /root/HadoopStreaming_Month
```

