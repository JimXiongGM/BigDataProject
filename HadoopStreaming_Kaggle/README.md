# 使用Hadoop Streaming分析数据

[点击这里](https://github.com/daviddwlee84/RaspPi-Cluster/tree/master/Example/MapReduce/GeneralWordCount)可以看到实现worldcount的mapper-reducer函数，推荐读者先理解原理，再看本文会更好理解一些。  

## 目录

> - [数据准备](#1)  
> - [描述性统计](#2)  
> - [提交到云端](#3)  
> - [下载结果](#4)  
> - [失败调试](#5)  

## <p id=1>数据准备 

这里使用的数据是kaggle的Amazon sales rank data for print and kindle books，详情可见[说明文档](../Documentations/open_datas.md)。[点击这里](../Documentations/Hadoop_distribute.md)可以看到这里的云端分布式配置详情。   

在说明文档中，数据已经被上传到HDFS。

首先，我们需要构思想要什么，从而构造mapper与reducer函数。那么我们可以从数据的描述性统计开始。

## <p id=2>描述性统计

这一部分的源代码分别对应当前目录下的[mapper_kaggle_1.py](./mapper_kaggle_1.py)和[reducer_kaggle_1.py](./reducer_kaggle_1.py)。  

#### mapper

我们首先需要知道，每一本书分别记录了多少个时间戳？分别的开始结束时间是多少？每一个mapper的输入是一个json文件，那么输出的形式就应该是<书ID，时间戳数量>、<书ID，开始时间>、<书ID，结束时间>。这里为了用上统计功能，加上了判断某本书是否在`2017-10-31`有取值的变动，即输出<'2017-10-31',True/False>。  

这里的意思是这样的：Map-Reduce框架的基本流程是，存在许多mapper和许多reducer，每个mapper可能产生多个<key,value>，不同的mapper可以产生相同的key，经过shuffle之后，相同的key到达相同的reducer，进行合并操作。因此本文构建`<'2017-10-31',True/False>`这样的键值对，不同的json进入不同的mapper，就能够产生相同的key，即`'2017-10-31'`。  

代码可以在当前目录找到，我们可以在bash中使用标准流进行测试。打开bash，进入这里的目录，输入`echo '{"1509379200":327588,"1509386400":348041,"1509393600":353297,"1509404400":369732}'  | ./mapper_kaggle_1.py;`，输出如下
```
root@master:~/gmfile/HadoopStreaming_Kaggle# echo '{"1509379200":327588,"1509386400":348041,"1509393600":353297,"1509404400":369732}'  | ./mapper_kaggle_1.py;
filename_test_307_len   4
filename_test_307_first 2017-10-31_00:00:00
filename_test_307_last  2017-10-31_07:00:00
2017-10-31      1
```
可以看到这里的一个mapper，输出了4个K-V对。  

特别说明的是，使用echo从文件产生流，但是我们并不能知道json文件的文件名，而这里的数据集使用每一本书的ID给每一个json文件命名。为了本地测试能够产生一个书本ID，这里使用随机整数的后缀来标识。


#### reducer

reducer稍微复杂一点。首先对每一个传入的流进行key-value切分。以上文的mapper函数输出为例，这里的输入就是四个K-V对。此外我们假设别的mapper也产生了`<'2017-10-31':1'>`，那么假设mapper产生的流如下
```
<'filename_test_180_len':'4'>
<'filename_test_180_first':'2017-10-31_00:00:00'>
<'filename_test_180_last':'2017-10-31_07:00:00'>
<'2017-10-31':1>
.
.
.
<'2017-10-31':1>
```
前三个不需要处理，只有最后一个需要相加，即需要产生`<'2017-10-31':2>`。因此，在reducer函数的IF部分，需要加上单独的判断条件。  


reducer.py中是如何判断key值的边界？Hadoop会在mapper的输出结果中对key进行排序，因此传到reducer部分的key值一定是连续的。所以reducer可以判断，只要传入key（`key`）不等于正在统计的key（`current_key`），那么进行下一个key的计算。  

我们可以在本地进行简单测试，使用命令`echo '{"1509379200":327588,"1509386400":348041,"1509393600":353297,"1509404400":369732}'  | ./mapper_kaggle_1.py | sort -t ' ' -k 1 | ./reducer_kaggle_1.py`即可，输出如下
```
root@master:~/gmfile/HadoopStreaming_Kaggle#  echo '{"1509379200":327588,"1509386400":348041,"1509393600":353297,"1509404400":369732}'  | ./mapper_kaggle_1.py | sort -t ' ' -k 1 | ./reducer_kaggle_1.py
2017-10-31      1
filename_test_894_first 2017-10-31_00:00:00
filename_test_894_last  2017-10-31_07:00:00
filename_test_894_len   4
```

如果使用目录下的真实文件测试，`cat 000721393X_com_norm.json | ./mapper_kaggle_1.py | sort -t ' ' -k 1 | ./reducer_kaggle_1.py`，即可看到有意思的结果，书000721393X的开始结束时间如下，在2017-10-31没有记录，一共记录次数是2730.
```
root@master:~/gmfile/HadoopStreaming_Kaggle#  cat 000721393X_com_norm.json |  ./mapper_kaggle_1.py | sort -t ' ' -k 1 | ./reducer_kaggle_1.py
2017-10-31      0
filename_test_960_first 2017-07-26_02:00:00
filename_test_960_last  2018-06-30_08:00:00
filename_test_960_len   2730
```

值得注意的是，这里使用到了linux的sort命令，[点击这里](https://www.cnblogs.com/fulucky/p/8022718.html)可以看到sort命令的基本用法。

## <p id=3>提交到云端


进入py文件所在的目录，使用如下命令即可。
```s
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar \
  -D mapreduce.job.name='KaggleTest01' \
  -input /Data_Sample/Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books/Sample_ranks_norm/*.json \
  -output /xgm/output/kaggle_01 \
  -mapper mapper_kaggle_1.py \
  -reducer reducer_kaggle_1.py \
  -file /root/gmfile/HadoopStreaming_Kaggle/mapper_kaggle_1.py \
  -file /root/gmfile/HadoopStreaming_Kaggle/reducer_kaggle_1.py
```
等待一段时间后，可以看到运行成功。


## <p id=4>下载结果

将结果从HDFS中拿出。
```

```





## <p id=5>失败调试

如果失败，分析思路可以参考笔者之前搭建平台的文章：[Hadoop3全分布式+Hadoop streaming环境搭建](../Documentations/Hadoop_distribute.md)



