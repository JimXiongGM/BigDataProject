# Spark Streaming基础

同之前。本章的所有内容均摘自机械工业出版社的《Spark大数据分析核心概念技术及实践》，提倡读者购买正版。本章的内容不适合直接阅读，应在阅读原书的基础上，直接run本章摘录、清洗好的代码，以加深印象。本章只作为一个索引，供复习使用。

## 目录



## 简介

这是一个分布式数据流处理框架，能够几乎实时地处理大量的数据流。

### API 

SparkStreaming API 有两个关键抽象 StreamingContext 和离散流 。 Spark Streaming 应用
可以使用这两个抽象来处理数据流 。

##  StreamingContext

StreamingContext 是一个在 Spark Streaming 库中定义的类，它是 Spark Streaming 库
的入口点。每一个 Spark Streaming 应用都必须创建一个 StreamingContext 类实例 。

### 创建 StreamingContext 实例

创建 StreamingContext 类实例类似于创建 SparkContext 类实例 。 可以使用和l 创建
SparkContext 类实例同样的参数来创建 StreamingContext 类实例 。 然而，它还有额外的参
数用于指定将数据流分割成批的时间间隔 。

```
import org.apache.spark.
import org.apache.spark.streaming._
val config = new SparkConf().setMaster("spark://host:port").setAppName("big streaming app")
val batchInterval = 10
val ssc = new StreamingContext(conf, Seconds(batchInterval))
```
如果已经有了 SparkContext 类实例，可以用它来创建 StreamingContext 类实例 。
```
import org.apache.spark._
import org.apache.spark.streaming._
val config = new SparkConf().setMaster("spark://host:port").setAppName("big streaming app")
val sc = new SparkContext(conf)
val batch!nterval = 10
val ssc = new StreamingContext(sc, Seconds(batch!nterval))
```
上面的例子中每一批的时间间隔为 10 秒钟 。 Spark Streaming 将每 10 秒钟从数据流源创建一个 RDD

### 开始流式计算

Spark Streaming 应用只有在调用了 start 方法之后，才会开始接收数据 。

```
ssc.start()
```

### 检查点

```
ssc.checkpoint("hdfs://master:9000/...")
```

### 停止流式计算

这个方法有一个可选参数，标识是否只关闭 StreamingContext 对象. 在 StreamingContext对象关闭的情况下， SparkContext 可以用来创建另外一个 StreamingContext 类实例

```
ssc.stop(true)
```

### 等待流式计算结束

如果应用是多线程的，井且调用 start 方法的是其他线程．而不是主线程．此时必须使用 awaitTermination 方法 。 StreamingContext 中的 start 方法是一个阻 塞 方法，直到流式计算结束或停止，这个方法才返回 。 如果应用是单线程的，主线程会一直等待 start 方法返回 。然而，如果是其他线程调用了 start 方法，那么在主线程中你就必须调用awaitTermination方法以避免主线程过早退出.

```
ssc.awaitTermination()
```
## Spark Streaming 应用基本结构

```
import org.apache.spark._
import org.apache.spark.streaming._

object StreamProcessingApp {
    def main(args : Array[String]):Unit = {
        val interval = args(0).toInt
        val conf = new SparkConf()
        val ssc = new StreamingContext(conf,Seconds(interval))

        // add your code here

        ssc.start()
        ssc.awaitTermination()
    }
}
```
## DStream

DStream 是 Spark Streaming 库中定义的一个抽象类 。DStreamis 是一个无穷无尽的 RDD 序列.

### 基本源

socketTextStream

textFileStream

actorStream

### 高级源

Spark Streaming 本身不提供诸如Kafka 、 Flume 或 Twitter 这样的高级源创建 DStream
的工厂方法 ，只有第三方库才提供 。

```
import org.apache.spark.streaming.twitter._
val tweets = TwitterUtils.createStream(ssc, None)
```

## 处理数据流

DStream 提供了两类操作：转换和输出操作 。 转换可以进一步细分成如下几类：基本转换、聚合转换、键值对转换 、特殊转换 。

### 基本转换

map

flatMap

filte

repartition

union

### 聚合转换

count

reduce

countByValue


### 键值对转换

cogroup

join

groupByKey

reduceByKey

### 特殊转换

transform

updateStateByKey

## 输出操作













