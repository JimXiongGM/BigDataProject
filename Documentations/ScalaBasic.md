# Scala语法基础

本章的所有内容均摘自机械工业出版社的《Spark大数据分析核心概念技术及实践》，提倡读者购买正版。本章的内容不适合直接阅读，应在阅读原书的基础上，直接run本章摘录、清洗好的代码，以加深印象。本章只作为一个索引，供复习使用。

## 目录

- [变量](#1)   
- [函数](#2)   
- [高阶方法](#3)   
- [类](#4)   
- [单例](#5)   
- [样本类](#6)   
- [模式匹配](#7)   
- [操作符](#8)   
- [特质](#9)   
- [元组](#10)   
- [Option类型](#11)   
- [集合](#12)   
- [集合类上的高阶方法](#13)   
- [一个单独的Scala应用程序](#14)   


## <p id=1>变量

变量类型 | 描 述
--- | ---
Byte |8 位有符号整数
Short |16 位有符号整数
Int |32 位有符号整数
Long |64 位有符号整数
Float |32位单精度浮点数
Double |32 位双精度浮点数
Char |16 位无符号
Unicode |字符
String |字符串
Boolean |true 或 false

## <p id=2>函数


```
def add(firstinput: Int, secondinput: Int): Int= {
val sum = firstinput + secondinput
return sum
}

def add(firstinput: Int, secondinput : Int) = firstinput + secondinput

```

## <p id=3>高阶方法

def encode(n: Int, f: (Int) => Long): Long= {
val x = n * 10
f(x)
}

### 函数字面量

函数字面量是指源代码中的匿名函数

```
(x: Int) => x + 100
val code = encode(10, (x: Int) => x + 100)

```

### 闭包


Scala中函数字面量却可以使用其所处作用域中的变量.

```
def encodeWithSeed(num: Int, seed: Int): Long= {
def encode(x: Int, func: (Int) => Int): Long= {
val y = x + 1000
func(y)
}
val result = encode( num( n: Int) => (n * seed))
result
}


```


## <p id=4>类


```
class Car(mk: String, ml: String, cr : String) {
val make = mk
val model = ml
var color = cr
def repaint(newColor : String) = {
color = newColor
}
}

```

类实例使用关键宇new创建.

```
val mustang = new Car("Ford","Mustang", "Red")
val corvette = new Car ("GM","Corvette","Black")

```

## <p id=5>单例

在面向对象编程中一个常见的设计模式就是单例,它是指那些只可以实例化一次的类Scala使用关键字object来定义单例对象.

## <p id=6>样本类

样本类是指使用case修饰符的类,下面是一个例子.样本类参数列表中的所有参数隐式获得val前缀的样本类 Message当成如下定义
```
case class Message(from: String, to: String, content: String)
val request = Message("harry","sam","fight")
```

## <p id=7>模式匹配

模式匹配是Scala中的概念,它看上去类似于其他语言的switch语句.
```
def colorToNumber(color: String): Int = {
val num = color match {
case "Red" => 1
case "Blue" => 2
case "Green" => 3
case "Yellow" => 4
case _ => 0
}
num
}
val x = colorToNumber("Green")

```

## <p id=8>操作符

Scala为基础类型提供了丰富的操作符.然而,Scala没有内置操作符.在Scala中,每一个基础类型都是一个类,每一个操作符都是一个方法.使用操作符等价于调用方法.
```
val x = 2
val y = 7
val z = x.+(y)

```

## <p id=9>特质
特质是类继承关系中的接口 . 

```
trait Shape {
def area(): Int
}

class Square(length: Int) extends Shape {
def area = length * length
}

class Rectangle(length: Int, width: Int) extends Shape {
def area = length * width
}

val square = new Square(10)
val area = square.area

```

## <p id=10>元组

元组是一个容器,用于存放两个或多个不同类型的元素.它是不可变的.它自从创建之后就不能修改了.

```
val twoElements = ("10", true)
val threeElements = ("10", "harry",true)

```

## <p id=11>Option类型

Option是一种数据类型,用来表示值是可选的,即要么无值要么有值.它要么是样本类Some的实例,要么是单例对象None的实例.

```
def colorCode(color: String): Option[Int] = {
color match {
case "red" => Some(1)
case "blue" => Some(2)
case "Green" => Some(3)
case _ => None
}
}
val code = colorCode("Green")
code match {
case Some(w) => println("code for orange is: "+ w)
case None => println("code not defined for orange")
}

```

## <p id=12>集合

Scala 的集合类可以分为 三类:序列､集合､ map.

### 序列


### 数组
数组是一个有索引的元素序列.数组中的所有元素都是相同类型的.它是,可变的数据结构.可以修改数组中的元素,但是你不能在它创建之后增加元素.它是定长的.
```
val arr = Array(10,20, 30, 40)
arr(0) = 50
val first = arr(0)

```

### 列表

列表是一个线性的元素序列,其中存放一堆相同类型的元素.它是一种递归的结构,而不像数组(扁平的数据结构).和数组不同,它是不可变的,创建后即不可修改.
```
val xs = List(10,20,30,40)
val ys = (1 to 10).toList
val zs = arr.toList

```


### 向量
向量是一个结合了列表和数组各自特性的类.它拥有数组和列表各自的性能优点.根据索引访问元素占用固定的时·间,线性访问元素也占用固定的时间.向量支持快速修改和访问任意位置的元素.
```
val vl = Vector(0, 10, 20, 30, 40)
val v2 = vl :+ 50
val v3 = v2:+60
val v4 = v3(4)
val vs = v3(5)

```


```
scala> val vl = Vector(0, 10, 20, 30, 40)
vl: scala.collection.immutable.Vector[Int] = Vector(0, 10, 20, 30, 40)

scala> val v2 = vl :+ 50
v2: scala.collection.immutable.Vector[Int] = Vector(0, 10, 20, 30, 40, 50)

scala> val v3 = v2:+60
v3: scala.collection.immutable.Vector[Int] = Vector(0, 10, 20, 30, 40, 50, 60)

scala> val v4 = v3(4)
v4: Int = 40

scala> val vs = v3(5)
vs: Int = 50


```

### 集合
集合是一个无序的集合.其中的每一个元素都不同.它没有重复的元素,而且,也没法通过索引来访问元素,因为它没有索引.

```
val fruits = Set("apple","orange","pear","banana")


```


### map
map是一个键-值对集合.在其他语言中,它也叫作字典
```
val capitals = Map ("USA" -> "Washington D.C." , "UK" -> "London" , "India" -> "New Delhi")
val indiaCapital = capitals("India")

```


## <p id=13>集合类上的高阶方法

高阶方法把函数当成参数.这些高阶方法并没有改变集合.所有的 Scala 集合类都支持这些高阶方法

### map




```
val xs = List(1, 2, 3, 4)
val ys = xs.map((x: Int) => x * 10.0)

val ys = xs map {x => x * 10.0}
val ys = xs.map {_ * 10.0}

```

### flatMap

Scala集合的flatMap方法类似于map,它的参数是一个函数,它把这个函数作用于集合中的每一个元素,返回另外一个集合c这个函数作用于原集合中的一个元素之后会返回一个集合.这样.最后就会得到一个元素都是集合的集合
```
val line = "Scala is fun"
val SingleSpace = " "
val words = line.split(SingleSpace)
val arrayOfChars = words flatMap {_.toList}

```


```
scala> val line = "Scala is fun"
line: String = Scala is fun

scala> val SingleSpace = " "
SingleSpace: String = " "

scala> val words = line.split(SingleSpace)
words: Array[String] = Array(Scala, is, fun)

scala> val arrayOfChars = words flatMap {_.toList}
arrayOfChars: Array[Char] = Array(S, c, a, l, a, i, s, f, u, n)


```


### filter

filter方法将谓词函数作用于集合中的每个元素,返回另一个集合,其中只包含计算结果为真的元素.谓词函数指的是返回一个布尔值的函数.它要么返回true,要么返回falseo
```
val xs = (1 to 100).toList
val even = xs filter {_%2 == 0}

```


### foreach

foreach方法的参数是-个函数,它把这个函数作用于集合中的每一个元素,但是不返回任何东西.它和map类似,唯一的区别在于map返回一个集合,而foreach不返回任何东西.由于它的无返回值特性它很少使用
```
val words = "Scala is fun".split(" ")
words.foreach(println)

```

### reduce

reduce方法返回一个值.顾名思义,它将一个集合整合成一个值.它的参数是一个函数,这个函数有两个参数,并返回一个值.从本质上说,这个函数是一个二元操作符,并且满足结合律和交换律.
```
val xs =List(2,4,6,8,10)
val sum = xs reduce {(x,y) => x+y}
val product = xs reduce {(x,y)=>x*y}
val max = xs reduce {(x,y) => if (x>y) x else y}
val min = xs reduce {(x,y) => if (x<y) x else y}

```


```
scala> val xs =List(2,4,6,8,10)
xs: List[Int] = List(2, 4, 6, 8, 10)

scala> val sum = xs reduce {(x,y) => x+y}
sum: Int = 30

scala> val product = xs reduce {(x,y)=>x*y}
product: Int = 3840

scala> val max = xs reduce {(x,y) => if (x>y) x else y}
max: Int = 10

scala> val min = xs reduce {(x,y) => if (x<y) x else y}
min: Int = 2


```

下面是一个找出句子中最长单词的例子 .

```
val words = "Scala is fun" split(" ")
val longestWord = words reduce {(wl, w2) => if(wl.length > w2.length) wl else w2}

```


```
scala> val words = "Scala is fun" split(" ")
words: Array[String] = Array(Scala, is, fun)

scala> val longestWord = words reduce {(wl, w2) => if(wl.length > w2.length) wl else w2}
longestWord: String = Scala

```

## <p id=14>一个单独的Scala应用程序

一个单独的Scala应用程序需要一个具有main方法的单例对象.这个main方法以一个Array[String]类型的参数作为输入.HelloWorld.scala
```
object HelloWorld {def main(args: Array[String]) : Unit = {println("Hello World !")}}
```
