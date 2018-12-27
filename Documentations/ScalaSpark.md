# Scala + Spark基础

本章的所有内容均摘自机械工业出版社的《Spark大数据分析核心概念技术及实践》，提倡读者购买正版。本章的内容不适合直接阅读，应在阅读原书的基础上，直接run本章摘录、清洗好的代码，以加深印象。本章只作为一个索引，供复习使用。

## 目录

- [Spark特点](#1)  
- [SparkContext](#2)  
- [RDD](#3)  
- [创建RDD](#4)  
- [RDD操作](#5)  
- [保存RDD](#6)  
- [惰性操作](#7)  
- [缓存](#8)  
- [共享变量](#9)  
- [Spark Shell](#10)  
- [编写Spark应用](#11)  
- - [安装sbt环境](#11-1)
- - [编译应用](#11-2)
- - [提交作业到集群](#11-3)


## <p id=1>Spark特点

Hadoop要求任何问题都必须能够分解为一系列的map作业和reduce作业.Spark提供的操作符来处理复杂的数据显得更加简单

### 快速

Spark要比Hadoop快若干个数量级，如果数据都加载在内存中，它能快上数百倍，哪怕数据元法完全载入内存，Spark也能快上数十倍

Spark比Hadoop快的原因有两方面，一方面，它可以使用基于内存的集群计算，另一方面.它实现了更先进的执行引擎

### 通用

Spark为各种类型的数据处理作业提供一个统一的集成平台.它可以用于批处理，交互分析，流处理，机器学习和图计算.相比之比，HadoopMapReduce只适合批处理.

### 集群管理员

Spark目前支持三种集群管理员:单独模式，Mesos模式，YARN模式.Mesas模式和YARN模式都允许在同一个worker节点上同时运行Spark应用和Hadoop应用.

### 数据源

任何Hadoop支持的数据源都可以被SparkCore使用
如果现有的Hadoop集群正在执行MapReduce作业，也可以同时在上面运行Spark应用.可以把现有的MapReduce作业转化成Spark作业.或者.也可以保留现有的MapReduce应用程序，不做更改，使用Spark运行新的应用程序.

### API

SparkAPI提供了如下语言的支持：Scala、Java、Python和R.

## <p id=2>SparkContext

SparkContext是一个在Spark库中定义的类.它是Spark库的入口点.它表示与Spark集群的一个连接.使用SparkAPI创建的其他一些重要对象都依赖于它.每个Spark应用程序都必须创建一个SparkContext类实例.目前，每个Spark应用程序只能拥有一个激活的SparkContext类实例.如果要创建一个新的实例，那么在此之前必须让当前激活的类实例失活.SparkContext有多个构造函数.最简单的一个不需要任何参数.一个SparkContext类实例可以用如下代码创建
```
val sc=new SparkContext()
```
在这种情况下，SparkContext的配置信息都从系统属性中获取，比如Sparkmaster的地址，应用名称等.也可以创建一个SparkConf类实例，然后把它作为SparkContext的参数从而设定配置信息.SparkConf是Spark库中定义的一个类.通过这种方式可以像下面这样设置各种Spark配置信息.

```
val config=new SparkConf().setMaster("spark://host:port").setAppName("bigapp")
val sc=new SparkContext(config)
```

SparkConf为设置诸如Sparkmaster这样的常用配置信息都提供了对应的显式方法.此外，它还提供了一个通用的方法用于设置配置信息，它使用键-值对进行设置.SparkContext和SparkConf可以使用的参数将在第4章进行详细介绍.

## <p id=3>RDD

弹性分布式数据集(RDD)表示一个关于分区数据元素的集合，可以在其上进行并行操作.它是Spark的主要数据抽象概念.它是Spark库中定义的一个抽象类.

### 不可变性
RDD是一种不可变的数据结构.一旦创建，它将不可以在原地修改.基本上，一个修改RDD的操作都会返回一个新的RDD.
### 分片

RDD表示的是一组数据的分区.这些分区分布在多个集群节点上.Spark存储RDD的分区和数据集物理分区之间关系的映射关系.RDD是各个分布式数据源之中数据的一个抽象，它通常表示分布在多个集群节点上的分区数据.

### 容错性

RDD会自动处理节点出故障的情况。

### 接口

RDD为多种数据提供了一个处理的统一接口

### 强类型

RDD类有一个参数用于表示类型，这使得RDD可以表示不同类型的数据.RDD可以表示同一类型数据的分布式集合，包括Integer，Long，Float，String或者应用开发者自己定义的类型。

### 驻留在内存中

Spark 允许 RDD 在内存中缓存或长期驻留 。

## <p id=4>创建RDD

> - parallelize

```
val xs = (1 to 10000).toList
val rdd = sc.parallelize(xs)
```
这个方法用于从本地Scala集合创建RDD实例.它会对Scala集合中的数据重新分区，重新分布，然后退回一个代表这些数据的RDD.

> - textFile

```
val rdd = sc. textFile("hdfs://namenode:9000/path/to/file-or-directory")
val rdd = sc. textFile("hdfs://namenode:9000/path/to/directory/*.gz")
```
textFile方法用于从文本文件创建RDD实例.这个方法返回一个RDD，这个RDD代表的数据集每个元素都是一个字符串，每一个字符串代表输入文件中的一行.textFile方法也可以读取压缩文件中的数据.而且，它的参数中可以存在通配符，用于从一个目录中读取多个文件.

> - wholeTextFiles

这个方法读取目录下的所有文本文件，然后返回一个由键值型RDD.返回RDD中的每一个键值对对应一个文件.键为文件路径，对应的值为该文件的内容.
```
val rdd = sc.wholeTextFiles("./*.txt")
```

> - sequenceFile

sequenceFile方法从SequenceFile文件中获取键值对数据.这个方法返回一个键值对型RDD实例.当使用这个方法的时候，不仅需要提供文件名，还需要提供文件中数据键和值各自的类型.


## <p id=5>RDD操作

RDD操作可以归为两类:转换和行动.转换将会创建一个新的RDD实例.行动则会将结果返回给驱动程序.
###  转换

区别:  
1. Scala 集合方法操作的数据是在单机内存中的，而RDD的转换操作可以处理分布在集群各个节点上的数据.  

2. RDD转换操作是惰性的，而Scala集合方法不是.

> - map

```
val lines= sc.textFile("...")
val lengths = lines map { l => l.length}
```

> - filter  

```
val lines = sc.textFile("...")
val longlines = lines filter { l => l.length > 80}
```

> - flatMap

对RDD中每个元素返回一个序列.扁平化这个序列的集合得到一个数据集

```
val lines = sc.textFile("...")
val words = lines flatMap { l => l.split(" ")}
```

> - mapPartitions  

mapPartitions是一个高阶方法，它使你可以以分区的粒度来处理数据.相比于一次处理一个元素，mapPartitions一次处理处理一个分区，每个分区被当成-个迭代器.mapPartitions方法的函数参数把迭代器作为输入，返回另外一个迭代器作为输出.mapPartitions将自定义函数参数作用于每一个分区上，从而返回一个新RDD实例.
```
val lines = sc.textFile("...")
val lengths = lines mapPartitions { iter => iter.map { l => l.length}}
```

> - union

取并集

```
val linesFile1 = sc.textFile("...")
val linesFile2 = sc.textFile("...")
val linesFromBothFiles = linesFile1.union(linesFile2)
```
> - intersection

取交集

```
val linesFile1 = sc.textFile("...")
val linesFile2 = sc.textFile("...")
val linesPresentinBothFiles = linesFile1.intersection(linesFile2)

val mammals = sc.parallelize(List("Lion","Dolphin","Whale"))
val aquatics =sc.parallelize(List("Shark","Dolphin","Whale"))
val aquaticMammals = mammals.intersection(aquatics)
```
> - subtract

减去子集，取补集

```
val linesFile1 = sc.textFile("...")
val linesFile2 = sc.textFile("...")
val linesInFile1Only = linesFile1.subtract(linesFile2)

val mammals = sc.parallelize(List("Lion","Dolphin", "Whale"))
val aquatics =sc.parallelize(List("Shark","Dolphin","Whale"))
val fishes = aquatics.subtract(mammals)
```
> - distinct

去重

```
val numbers = sc.parallelize(List(l, 2, 3, 4, 3, 2, 1))
val uniqueNumbers = numbers.distinct
```

> - cartesian

笛卡尔积.返回的RDD实例的每一个元素都是一个有序二元组，每一个有序二元组的第一个元素来自原RDD，第二个元素来自输入RDD.元素的个数等于原RDD的元素个数乘以输入RDD的元素个数.这个方法类似于SQL中的join操作.

```
val numbers = sc.parallelize(List(l, 2, 3, 4))
val alphabets = sc. parallelize( List ("a","b","E","d"))
val cartesianPRDDuct = numbers.cartesian(alphabets)
```

> - zip  

新RDD实例的每一个元素是一个二元组.二元组的第一个元素来自原RDD，第二个元素来自输入RDD.和cartesian方法不同的是，zip方法返回的RDD的元素个数于原RDD的元素个数.原RDD的元素个数和输入RDD的相同.进一步地说，原RDD和输入RDD不仅有相同的分区数，每个分区还有相同的元素个数。

```
val numbers = sc.parallelize(List(1, 2, 3, 4))
val alphabets = sc.parallelize(List("a","b", "c"," d"))
val zippedPairs = numbers.zip(alphabets)
```

> - zipWithlndex  

新RDD实例的每个元素都是由原RDD元素及其下标构成的二元组.
```
val alphabets = sc.parallelize(List("a","b","c","d"))
val alphabetsWithindex = alphabets.zip
```

> - groupBy  

groupBy是一个高阶方法，它将原RDD中的元素按照用户定义的标准分组从而组成一个RDD.它把一个函数作为它的参数，这个函数为原RDD中的每一个元素生成一个键.groupBy把这个函数作用在原RDD的每一个元素上，然后返回一个由二元组构成的新RDD实例，每个二元组的第一个元素是函数生成的键，第二个元素是对应这个键的所有原RDD元素的集合.其中，键和原RDD元素的对应关系由那个作为参数的函数决定.  

需要注意的是，groupBy是一个费时操作，因为它可能需要对数据做shuffle操作.假设有一个csv文件，文件的内容为公司客户的姓名，年龄，性别和邮编.下面的示例代码演示了按照邮编将客户分组 。

```
case class Customer(name: String, age: Int, gender: String, zip: String)
val lines = sc.textFile("...")
val customers = lines map { l => {
	val a = l.split(",")
	Customer(a(0),a(1).toInt,a(2),a(3))
	}
	}
val groupByZip = customers.groupBy { c => c.zip}
```
> - keyBy

groupBy和KeyBy的区别在于返回RDD实例的元素上.虽然都是二元组，但是groupBy返回的二元组中的第二个元素是一个集合，而keyBy的是单个值.
```
case class Person(name: String, age: Int, gender: String, zip: String)
val lines = sc. textFile("...")
val people = lines map { l => {
val a = l.split(",")
Person(a(0), a(1).toInt, a(2), a(3))
}
}
val keyedByZip = people.keyBy{p => p.zip}
```

> - sortBy

sortBy是一个高阶方法，它将原RDD中的元素进行排序后组成一个新的RDD实例返回.它拥有两个参数.第一个参数是一个函数，这个函数将为原RDD的每一个元素生成一个键.第二个参数用来指明是升序还是降序排列.
```
val numbers = sc.parallelize(List(3,2,4,1,5))
val sorted = numbers.sortBy(x => x, true)

case class Person(name: String, age: Int, gender: String, zip: String)
val lines = sc. textFile("...")
val people = lines map { 1 => {
val a = l.split(",")
Person(a(0), a(l).toInt,a(2),a(3))
}
}
val sortedByAge = people.sortBy(p => p.age,true)
```

> - pipe

pipe方法可以让你创建子进程来运行一段外部程序，然后捕获它的输出作为字符串，用这些字符串构成RDD实例返回.> - randomSplit   

randomSplit方法将原RDD分解成一个RDD数组.它的参数是分解的权重.

```
val numbers = sc. parallelize((1 to 100).toList)
val splits = numbers.randomSplit(Array(0.6,0.2,0.2))
```

> - coalesce

coalesce方法用于减少RDD的分区数量.它把分区数作为参数，返回分区数等于这个参数的RDD实例.使用coalesce方法时需要小心，因为减少了RDD的分区数也就意味着降低了Spark的并行能力.它通常用于合井小分区.  

举例来说，在执行flter操作之后，RDD可能会有很多小分区.在这种情况下，减少分区数能提升性能.
```
val numbers = sc.parallelize((1 to 100).toList)
val numbersWithOnePartition = numbers.coalesce(1)
```

> - repartition

repartition方法把一个整数作为参数，返回分区数等于这个参数的RDD实例.它有助于提高Spark的并行能力.它会重新分布数据，因此它是一个耗时操作.  

coalesce和repartition方法看起来一样，但是前者用于减少RDD中的分区，后者用于增加RDD中的分区.

```
val numbers = sc.parallelize((l to 100).toList)
val numbersWithOnePartition = numbers.repartition(4)
```

> - sample

sample方法返回原RDD数据集的一个抽样子集.它拥有三个参数.第一个参数指定是有放回抽样还是无放回抽样.第二个参数指定抽样比例.第三个参数是可选的，指定抽样的随机数种子.
```
val numbers = sc.parallelize((l to 100).toList)
val sampleNumbers = numbers.sample(true, 0.2)
```

###  键值对型 RDD 的转换

除了上面介绍的RDD转换之外，针对键值对型RDD还支持其他的一些转换.下面将介绍只能作用于键值对型RDD的常用转换操作.

> - keys

keys方法返回只由原RDD中的键构成的RDD.
```
val kvRdd = sc.parallelize(List(("a",1),("b",2),("c",3)))
val keysRdd = kvRdd.keys
```

> - values

```
val kvRdd = sc.parallelize(List(("a",1),("b",2),("c",3)))
val valuesRdd = kvRdd.values
```

> - mapValues

mapValues是一个高阶方法，它把一个函数作为它的参数，并把这个函数作用在原RDD的每个值上.它返回一个由键值对构成的RDDo.它和map方法类似，不同点在于它把作为参数的函数作用在原RDD的值上，所以原RDD的键都没有变.返回的RDD和原RDD拥有相同的键.

```
val kvRdd = sc.parallelize(List(("a",1),("b",2),("c",3)))
val valuesDoubled = kvRdd mapValues { x => 2*x}
```

> - join

join方法把一个键值对型RDD作为参数输入，而后在原RDD和输入RDD上做内连接操作.它返回一个由二元组构成的RDD.二元组的第一个元素是原RDD和输入RDD都有的键，第二个元素是一个元组，这个元组由原RDD和输入RDD中键对应的值构成.  

{  (key,(value1,value2)),(XXX,XXX)  }

```
val pairRdd1 = sc.parallelize(List(("a",1),("b",2),("c",3)))
val pairRdd2 = sc.parallelize(List(("b","second"),("c","third"),("d","fourth")))
val joinRdd = pairRdd1.join(pairRdd2)
```

> - leftOuterJoin

```
val pairRdd1 = sc.parallelize(List(("a",1),("b",2),("c",3)))
val pairRdd2 = sc.parallelize(List(("b","second"),("c","third"),("d","fourth")))
val leftOuterJoin = pairRdd1.leftOuterJoin(pairRdd2)
```

> - rightOuterJoin

```
val pairRdd1 = sc.parallelize(List(("a",1),("b",2),("c",3)))
val pairRdd2 = sc.parallelize(List(("b","second"),("c","third"),("d","fourth")))
val rightOuterJoin = pairRdd1.rightOuterJoin(pairRdd2)
```

> - fullOuterJoin

```
val pairRdd1 = sc.parallelize(List(("a",1),("b",2),("c",3)))
val pairRdd2 = sc.parallelize(List(("b","second"),("c","third"),("d","fourth")))
val fullOuterJoin = pairRdd1.fullOuterJoin(pairRdd2)
```

> - sampleByKey

sampleByKey通过在键上抽样返回原RDD的一个子集.它把对每个键的抽样比例作为输入参数.返回原RDD的一个抽样.
```
val pairRdd = sc.parallelize(List(("a",1),("b",2),("a",11),("b",22),("a",111),("b",222))
val sampleRdd = pairRdd.sampleByKey(true,Map("a"->0.1,"b"->0.2))
```

> - subtractByKey

减去输入，补集

```
val pairRdd1 = sc.parallelize(List(("a",1),("b",2),("c",3)))
val pairRdd2 = sc.parallelize(List(("b","second"),("c","third"),("d","fourth")))
val resultRDD = pairRdd1.subtractByKey(pairRdd2)
```

> - groupByKey

和之前的groupBy区别在于groupBy是一个高阶方法，它的参数是一个函数，这个函数为原RDD的每一个元素生成一个键.groupByKey方法作用于RDD的每一个键值对上，故不需要一个生成键的函数作为输入参数.
```
val pairRdd = sc.parallelize(List(("a",1),("b",2),("a",11),("b",22),("a",111),("b",222))
val groupedRdd = pairRdd.groupByKey()
```

> - reduceByKey

reduceByKey是一个高阶方法，它把一个满足结合律的二元操作符当作输入参数，把这个操作符作用于有相同键的值上.一个二元操作符把两个值当作输入参数，返回一个值.  

reduceByKey方法，可以用于对同一键对应的值进行汇总操作.比如它可以用于对同一健对应的值进行求和，求乘积，求最小值，求最大值.  

对于基于键的汇总操作，合并操作，reduceByKey比groupByKey更合适
```
val pairRdd = sc.parallelize(List(("a",1),("b",2),("a",11),("b",22),("a",111),("b",222))
val sumByKeyRdd = pairRdd.reduceByKey((x,y) => x+y)
val minByKeyRdd = pairRdd.reduceByKey((x,y) => if (x < y) x else y)
```

###  操作

操作指的是那些返回值给驱动程序的RDD方法.

> - collect

collect方法返回一个数组，这个数组由原RDD中的元素构成.在使用这个方法的时候需要小心，因为它把在worker节点的数据移给了驱动程序.如果操作一个有大数据集的RDD，它有可能会导致驱动程序崩溃.
```
val rdd = sc.parallelize((1 to 10000).toList)
val filteredRdd = rdd filter { x => (x % 1000) == 0}
val filterResult = filteredRdd.collect
```

> - count

```
val rdd = sc.parallelize((1 to 10000).toList)
val total = rdd.count
```

> - countByValue

countByValue方法返回原RDD中每个元素的个数.它返回是一个map类实例，其中，键为元素的值，值为该元素的个数.
```
val rdd = sc.parallelize(List(l,2,3,4,1,2,3,1,2,1))
val counts = rdd.countByValue
```

> - first

first方法返回原RDD中的第一个元素.
```
val rdd = sc.parallelize(List(10,5,3,1))
val firstElement = rdd.first
```

> - max

```
val rdd = sc.parallelize(List(2,5,3,1))
val maxElement = rdd.max
```

> - min

```
val rdd = sc.parallelize(List(2,5,3,1))
val minElement = rdd.min
```

> - take

take方法的输入参数为一个整数N，它返回一个由原RDD中前N个元素构成的RDD.
```
val rdd = sc.parallelize(List(2,5,3,1,50,100))
val first3 = rdd.take(3)
```

> - takeOrdered

takeOrdered方法的输入参数为一个整数N，它返回一个由原RDD中前N小的元素构成的RDD
```
val rdd = sc.parallelize(List(2,5,3,1,50,100))
val smallest3 = rdd.takeOrdered(3)
```

> - top

```
val rdd = sc.parallelize(List(2,5,3,1,50,100))
val largest3 = rdd.top(3)
```

> - fold

fold是一个高阶方法.用于对原RDD的元素做汇总操作，汇总的时候使用一个自定义的初值和一个满足结合律的二元操作符.它首先在每一个RDD的分区中进行汇总，然后再汇总这些结果 。

```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val sum= numbersRdd.fold(0) ((partialSum, x) => partialSum + x)
val pRDDuct = numbersRdd.fold(1) ((partialPRDDuct, x) => partialPRDDuct * x)
```

> - reduce

reduce是一个高阶方法，用于对原RDD的元素做汇总操作，汇总的时候使用一个满足结合律和交换律的二元操作符.它类似于fold方法，然而，它并不需要初值.
```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val sum = numbersRdd.reduce ((x, y) => x + y)
val pRDDuct = numbersRdd.reduce((x, y) => x * y)
```

###  键值对型 RDD 上的操作

键值对RDD上有一些额外的操作，我们在下面进行介绍.

> - countByKey

统计原RDD每个键的个数3它返回一个map类实例，其中，键为原RDD中的键，值为个数.
```
val pairRdd = sc.parallelize(List(("a",1),("b",2),("c",3),("a",11),("b",22),("a",1)))
val countOfEachKey = pairRdd.countByKey
```

> - lookup

lookup方法的输入参数为一个键，返回一个序列，这个序列的元素为原RDD中这个健对应的值.
```
val pairRdd = sc.parallelize(List(("a",1),("b",2),("c",3),("a",11),("b",22),("a",1)))
val values = pairRdd.lookup("a")
```

###  数值型 RDD 上的操作

如果RDD的元素类型为Integer，Long，Float或Double，则这样的RDD为数值型RDD.这类RDD还有一些对于统计分析十分有用的额外操作，下面将介绍一些常用的行动

> - mean

```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val mean = numbersRdd.mean
```

> - stdev

```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val stdev = numbersRdd.stdev
```

> - sum

```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val sum = numbersRdd.sum
```

> - variance

```
val numbersRdd = sc.parallelize(List(2,5,3,1))
val variance = numbersRdd.variance
```

## <p id=6>保存RDD

需要注意的是.下面的方法都把一个目录的名字作为输入参数，然后在这个目录为每个RDD分区创建一个文件.
> - saveAsTextFile

saveAsTextFile方法将原RDD中的元素保存在指定目录中，这个目录位于任何Hadoop支持的存储系统中.每一个RDD中的元素都用字符串表示并另存为文本中的一行.
```
val numbersRdd = sc.parallelize((1 to 10000).toList)
val filteredRdd = numbersRdd filter { x => x % 1000 == 0｝
filteredRdd.saveAsTextFile("numbers-as-text")
```

> - saveAsObjectFile

saveAsObjectFile方法将原RDD中的元素序列化成Java对象，存储在指定日录中.

```
val numbersRdd = sc.parallelize((1 to 10000).toList)
val filteredRdd = numbersRdd filter { x => x % 1000 == 0｝
filteredRdd.saveAsObjectFile("numbers-as-object")
```

> - saveAsSequenceFile

```
val pairs = (1 to 10000).toList map {x => (x, x*2)}
val pairsRdd = sc.parallelize(pairs)
val filteredPairsRdd = pairsRdd filter { case (x, y) => x % 1000 == 0 }
filteredPairsRdd.saveAsSequenceFile("pairs-as-sequence")
filteredPairsRdd.saveAsTextFile("pairs-as-text")
```

## <p id=7>惰性操作

当应用调用一个返回RDD的方法的时候.Spark并不会立即执行运算.比如，当你使用SparkContext的textFile方法从HDFS中读取文件时，Spark并不会马上从硬盘中读取文件.  

类似地，RDD转换操作(它会返回新RDD)也是惰性的.  

Spark仅仅记录了这个RDD是怎么创建的，在它上面做转换操作会创建怎样的子RDD等信息.Spark为每一个RDD维护其各自的血统信息.在需要的时候.Spark利用这些信息创建RDD或重建RDD.

### 触发计算的操作

当Spark应用调用操作方法或者保存RDD至存储系统的时候，RDD的转换计算才真正执行.

## <p id=8>缓存

创建RDD有两种方式.从存储系统中读取数据或者应用其他现存RDD的转换操作.
考虑下丽的例子，尽管上面的代码只调用了-次textFile方法，但是日志文件会被从硬盘中读取两次.这是因为调用了两次操作方法count.
```
val logs = sc.textFile("path/to/log-files")
val errorlogs = logs filter { l => l.contains("ERROR")}
val warninglogs = logs filter { l => l.contains("WARN")}
val errorCount = errorlogs.count
val warningCount = warninglogs.count
```

### RDD 的缓存方法

RDD提供了两种缓存方法:cache和persist

#### cache

cache方法把RDD存储在集群中执行者的内存中.它实际上是将RDD物化在内存中.下面的例子展示了怎么利用缓存优化上面的例子.

```
val logs = sc. textFile("path/to/log-files")
val errorsAndWarnings = logs filter { l => l.contains("ERROR") || l.contains("WARN")}
errorsAndWarnings.cache()
val errorLogs = errorsAndWarnings filter { l => l.contains("ERROR")}
val warninglogs = errorsAndWarnings filter { l => l.contains("WARN")}
val errorCount = errorlogs.count
val warningCount = warninglogs.count
```

#### persist

persist是一个通用版的cache方法.它把RDD存储在内存中或者硬盘上或者二者皆有.它的输入参数是存储等级，这是一个可选参数.如果调用persist方法而没有提供参数，那么它的行为类似于cache方法.

```
val lines= sc.textFile("...")
lines.persist(MEMORY_ONLY)
```

> - MEMORY_ONLY 

将RDD分区采用反序列化Java对象的方式存储在worker节点的内存中.如果一个RDD分区无法完全载入worker节点的内存中，那么它将在需要时才计算.
> - DISK_ONLY 

物化RDD分区，把它们存储在每一个worker节点的本地文件系统中.这个参数可以用于缓存中间的RDD，这样接下来的一系列操作就没必要从根RDD开始计算了.

> - MEMORY_AND_DISK 

尽可能地把RDD分区存储在内存中.如果有剩余.就把剩余的分区存储在硬盘上.> - MEMORY_ONLY_SER

采用序列化Java对象的方式将RDD分区存储在内存中G一个序列化的Java对象会消耗更少的内存，但是读取是CPU密集型的操作G这个参数是在内存消耗和CPU使用之间做的一个妥协.

> - MEMORY_AND_DISK_SER

尽可能地以序列化Java对象的方式将RDD分区存储在内存中.如果有剩余，则剩余的分区会存储在硬盘上.

## <p id=9>共享变量

Spark没有全局的内存空间用于任务间共享.驱动程序和任务之间通过消息共享数据.

### 广播变量

Spark只会给worker节点发送一次广播变量，并且将它反序列化成只读变量存储在执行者的内存中.而且，Spark采用一种更高效的算法来发布广播变量.  

SparkContext类提供了一个叫作broadcast的方法用于创建广播变量.它把一个待广播的变量作为参数，返回一个Broadcast类实例.一个任务必须使用Broadcast对象的value方法才可以获取广播变量的值.  

考虑这样一个应用，它根据电商交易信息生成交易详情.在现实世界的应用中会有一张顾客表，一张商品表和一张交易表.为了简化起见，我们直接用一些简单的数据结构来代替这些表作为输入数据.

```
case class Transaction(id: Long, custId: Int, itemId: Int)
case class TransactionDetail(id: Long, custName: String, itemName: String)

val customerMap = Map(1->"Tom", 2->"Harry")
val itemMap = Map(1->"Razor", 2->"Blade")
val transactions = sc.parallelize(List(Transaction(l,1,1),Transaction(2,1,2)))
val bcCustomerMap = sc.broadcast(customerMap)
val bcItemMap = sc.broadcast(itemMap)
val transactionDetails = transactions.map{t => TransactionDetail(
			t.id, bcCustomerMap.value(t.custId), bcItemMap.value(t.itemId))}
transactionDetails.collect
```

### 累加器

累加器是只增变量  

考虑这样一个应用，它需要从顾客表中过滤出不合法的顾客并计数.
```
case class Customer(id: Long, name: String)
val customers = sc.parallelize( List(
	Customer(1,"Tom"),
	Customer(2,"Harry"),
	Customer(-1,"Paul")))
val badIds = sc.accumulator(0,"Bad id accumulator")
val validCustomers = customers.filter(c => if (c.id < 0) {
			badIds += 1
			false
} else true
)
val validCustomerids = validCustomers.count
val invalidCustomerids = badIds.value
```

## <p id=10>Spark Shell

### REPL命令

> - `:help`  
> - `:quit`  
> - `:paste`  

输入:paste将进入粘贴模式.在粘贴模式中可以输入或者粘贴多行代码.当需要粘贴多行代码时，粘贴模式就显得特别有用.完成操作之后按Ctrl+D组合键表示结束.一旦按Ctrl+D组合键，Sparkshell就会对输入的多行代码块进行求值.

### 数值分析

从一个Scala集合创建RDD 

```
val xs = (1 to 1000).toList
val xsRdd = sc.parallelize(xs)
val evenRdd = xsRdd.filter{ _ % 2 == 0}
val count = evenRdd.count
val first = evenRdd.first
val firsts = evenRdd.take(5)
```

### 日志分析

```
val rawlogs = sc.textFile("data/app.log")
val rawlogs = sc.textFile("hdfs://data/app.log")
val logs = rawLogs.map {line => line.trim.toLowerCase()}
logs.persist()
val totalCount = logs.count()
val errorlogs = logs.filter{ line =>
	val words = line.split(" ")
	val loglevel = words(1)
	loglevel == "error"
	}
val errorlogs = logs.filter{_.split(" ")(1) == "error"}
val errorlogs = logs.filter{_.split("\\s+")(1) == "error"}
val errorCount = errorlogs.count()
val firstError = errorlogs.first()
val first3Errors = errorlogs.take(3)

val lengths = logs.map{line => line.size}
val maxlen = lengths.reduce{ (a, b) => if (a > b) a else b }

val wordCounts = logs map {line => line.split("""\s+""").size}
val maxWords = wordCounts reduce{ (a, b) => if (a > b) a else b }
```

利用函数来统计各个严重等级对应的日志条数.

```
:paste

def severity(log: String): String = {
	val columns = log.split("\\s+", 3)
	columns(1)
	}
val pairs = logs.map { log => (severity(log), 1)}
val countBySeverityRdd = pairs.reduceByKey{(x,y) => x + y}
val countBySeverity= countBySeverityRdd.collect()
countBySeverityRdd.saveAsTextFile("data/log-counts-text")
```

## <p id=11>编写Spark应用


### Spark中的Hello World

```
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

object WordCount {
	def main(args: Array[String]): Unit = {
	val inputPath = args(0)
	val outputPath = args(1)
	val sc = new SparkContext()
	val lines= sc.textFile(inputPath)
	val wordCounts = lines.flatMap {line => line.split(" ")}
		.map(word => (word, 1))
		.reduceByKey(_ + _)
	wordCounts.saveAsTextFile(outputPath)
	}
}
```
### <p id=11-1>安装sbt环境

scala文件需要使用sbt进行编译。Scala编译器会将Scala应用程序编译成Java字节码，Java字节码运行在JVM上。从字节码的层面来看，Scala应用程序和Java应用程序没有区别。这里我们首先要安装sbt。根据官网的[安装教程](https://www.scala-sbt.org/1.x/docs/Installing-sbt-on-Linux.html)以及项目之前的配置情况，直接在master端run以下code即可完成下载解压配置环境变量。

```
cd /root/xiazai;
wget https://sbt-downloads.cdnedge.bluemix.net/releases/v1.2.7/sbt-1.2.7.tgz;
tar -zxvf sbt-1.2.7.tgz;
mv sbt /opt/;
chmod u+x /opt/sbt;
echo 'export SBT_HOME=/opt/sbt' >> /etc/bash.bashrc;
echo 'export PATH=${SBT_HOME}/bin:$PATH' >> /etc/bash.bashrc;
source /etc/bash.bashrc;
sbt;
```


### <p id=#11-2>编译应用

为了运行应用WordCount，我们需要编译源代码，并把它打包成一个jar文件。用sbt的工具来构建。最后使用Spark自带的Spark-submit脚本来运行应用。  

使用如下命令建立`WordCount`文件目录并且创建scala文件、配置sbt文件并打包。
```bash
mkdir /root/WordCountSpark;
cd /root/WordCountSpark;
rm WordCount.scala
touch WordCount.scala;
echo 'import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
 
object WordCount {
    def main(args: Array[String]): Unit = {
    val inputPath = args(0)
    val outputPath = args(1)
    val sc = new SparkContext()
    val lines= sc.textFile(inputPath)
    val wordCounts = lines.flatMap {line => line.split(" ")}
        .map(word => (word, 1))
        .reduceByKey(_ + _)
    wordCounts.saveAsTextFile(outputPath)
    }
}' >> WordCount.scala;

echo "配置sbt文件";

rm BuildWordCount.sbt;
touch BuildWordCount.sbt;
echo 'ThisBuild / version := "1.0.0"
ThisBuild / scalaVersion := "2.11.12"
ThisBuild / organization := "xgm"

lazy val WordCountSpark = (project in file("."))
  .settings(
    name := "WordCountSpark",
    libraryDependencies += "org.apache.spark" %% "spark-core" % "2.4.0" % "provided"
  )' >> BuildWordCount.sbt;

sbt package;

```


等待一段时间后，出现如下即可成功
```
...
[info] Packaging /root/WordCountSpark/target/scala-2.12/worldcountspark_2.12-0.1.0-SNAPSHOT.jar ...
[info] Packaging /root/WordCountSpark/target/scala-2.12/worldcountspark_2.12-0.1.0-SNAPSHOT.jar ...
[info] Done packaging.
[success] Total time: 516 s, completed Dec 27, 2018 7:23:36 PM
```
使用`ls /WordCountSpark/target/scala-2.11`可以看到我们需要的`wordcountspark_2.11-1.0.0.jar`

这里遇到很迷的事。。。第一次执行`sbt package`的时候，出现`scala-2-11_2.12-0.1.0-SNAPSHOT.jar`，但是这个jar跑不通。再一次执行`sbt package`的时候，找到了`wordcountspark_2.11-1.0.0.jar`。笔者推测是这里的阿里云cpu配置不够，第一次没有编译完整，再一次编译即可成功。



### <p id=#11-3>提交作业到集群

#### 使用spark standalone

使用如下命令即可提交任务到spark自带的调度器，在`http://master:8080`可以看到任务的情况
```
$SPARK_HOME/bin/spark-submit --class "WordCount" --master spark://master:7077 \
/root/WordCountSpark/target/scala-2.11/wordcountspark_2.11-1.0.0.jar  \
hdfs://master:9000/data/WordCountDemo/test.txt \
hdfs://master:9000//xgm/output/Spark_WordCount01
```
同样，使用`hdfs dfs -tail /xgm/output/Spark_WordCount01/part-00000`即可查看我们的输出结果。


#### 使用YARN

copy+enter即可。
```
$SPARK_HOME/bin/spark-submit --class "WordCount" \
    --master yarn \
    --deploy-mode cluster \
    --driver-memory 512mb \
    --executor-memory 512mb \
    --executor-cores 1 \
    --queue default \
    /root/WordCountSpark/target/scala-2.11/wordcountspark_2.11-1.0.0.jar \
    hdfs://master:9000/data/WordCountDemo/test.txt \
    hdfs://master:9000//xgm/output/Spark_WordCount02
```


