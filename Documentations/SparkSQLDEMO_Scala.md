# Spark + SQL实例 (Scala + python3)

这一部分的内容没有参考之前的《Spark大数据分析核心概念技术及实践》，主要原因是笔者搭建的spark2.4.0API较新，将SparkContext等合并为SparkSession，变动较大。这里主要的参考材料是[官网文档](http://spark.apache.org/docs/latest/sql-getting-started.html)以及Tomasz Drabas编写的《PySpark实战指南》

## 目录 

- [CSV文件(scala)](#1)
- [CSV文件(python3)](#2)


## <p id=1>CSV文件(scala)

使用`$SPARK-HOME/bin/spark-shell --master spark://master:7077`命令打开spark-shell，可以整段copy+enter，也可以一条一条执行下面的命令。

这里的数据来源于HDFS，之前的文章已经上传了，分别在[公开数据介绍](./public_datas.md)和[私有数据介绍](./private_datas.md)能够看到详情
```js

val df1 = spark.read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").option("header", true).option("delimiter", ",").load("hdfs://master:9000/Data_Sample/Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books/amazon_com_extras.csv")

// df.show()
df1.printSchema()
df1.select("GROUP").show(10)
df1.select("FORMAT").show()
df1.select("TITLE").show(7)
df1.select($"GROUP", $"TITLE").show()

df1.select("GROUP","TITLE").filter("GROUP = 'kindle'").show(9)

// C开头的书
df1.select("GROUP","TITLE").filter("TITLE like 'C%'").show(9)

df1.filter($"GROUP" > "book").show(9)
df1.groupBy("GROUP").count().show()

df1.createOrReplaceTempView("amazon_book")
val sqldf2 = spark.sql("SELECT * FROM amazon_book WHERE GROUP>'book'")
sqldf2.show()

val sqldf1 = spark.sql("SELECT * FROM amazon_book WHERE TITLE like 'C%'")
sqldf1.show()
```

```js
scala> df1.printSchema()
root
 |-- ASIN: string (nullable = true)
 |-- GROUP: string (nullable = true)
 |-- FORMAT: string (nullable = true)
 |-- TITLE: string (nullable = true)
 |-- AUTHOR: string (nullable = true)
 |-- PUBLISHER: string (nullable = true)
```


## <p id=2>CSV文件(python3)

这一部分直接笔者直接在jupyter notebook上实现，安装过程点击[这里](./JupyterNotebook.md)，示例代码点击[这里](./TEST_PySpark.html)


## JSON文件

`caixin_125_0_100.json`文件是一种嵌套JSON结构，直接使用select会出问题。这里需要引入新的用法，参考资料来源[这里](https://cloud.tencent.com/developer/article/1032531)


```js
未完待续
```




```js
scala> df2.printSchema()
root
 |-- count: long (nullable = true)
 |-- datas: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- attr: long (nullable = true)
 |    |    |-- audioUrl: string (nullable = true)
 |    |    |-- cate: string (nullable = true)
 |    |    |-- channelDesc: string (nullable = true)
 |    |    |-- channelId: long (nullable = true)
 |    |    |-- comm: struct (nullable = true)
 |    |    |    |-- aid: string (nullable = true)
 |    |    |    |-- tid: string (nullable = true)
 |    |    |-- desc: string (nullable = true)
 |    |    |-- edit: struct (nullable = true)
 |    |    |    |-- desc: string (nullable = true)
 |    |    |    |-- head: string (nullable = true)
 |    |    |    |-- link: string (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |    |-- rank: string (nullable = true)
 |    |    |-- form: struct (nullable = true)
 |    |    |    |-- txt: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |    |-- freeDuration: string (nullable = true)
 |    |    |-- freeTime: string (nullable = true)
 |    |    |-- link: string (nullable = true)
 |    |    |-- nid: long (nullable = true)
 |    |    |-- pict: struct (nullable = true)
 |    |    |    |-- imgs: array (nullable = true)
 |    |    |    |    |-- element: struct (containsNull = true)
 |    |    |    |    |    |-- txt: string (nullable = true)
 |    |    |    |    |    |-- url: string (nullable = true)
 |    |    |    |-- num: long (nullable = true)
 |    |    |-- subDesc: string (nullable = true)
 |    |    |-- summ: string (nullable = true)
 |    |    |-- tags: array (nullable = true)
 |    |    |    |-- element: string (containsNull = true)
 |    |    |-- time: string (nullable = true)
 |    |    |-- type: long (nullable = true)
 |    |    |-- video: string (nullable = true)
 |-- maxes: long (nullable = true)
 |-- start: long (nullable = true)
```

在非shell环境的使用方法。

```py
import org.apache.spark.sql.SparkSession

val spark = SparkSession
  .builder()
  .appName("Spark SQL basic example")
  .config("spark.some.config.option", "some-value")
  .getOrCreate()

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._
```








