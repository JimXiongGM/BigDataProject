# 公开数据集介绍

这是笔者找的一些大小在1-10GB，包含结构化、半结构化、非结构化的公开数据集。[点击这里](../README.md)返回主目录。

## 目录

> - [Amazon sales rank data for print and kindle books](#1)  
> - [THUCNews数据集](#2)  
> - [全网新闻数据(SogouCA,2012)数据集](#3)  
> - [高频交易数据](#4)  


## <p id=1>Amazon sales rank data for print and kindle books

这是一份来自Kaggle的数据集，[点击这里](https://www.kaggle.com/ucffool/amazon-sales-rank-data-for-print-and-kindle-books)，这份数据集记录的是Amazon上的书,以及相应书目随时间变化的sale rank。考虑到国内下载网速较慢，笔者在百度网盘提供了备份，[点击这里](https://pan.baidu.com/s/1S5GkFcthv5pT_ZPyRz1ceA)可以获取，提取码: `8w26`。


### <p id=1-1>数据介绍</p>

这一份数据集包含两个文件夹以及三个说明文件，简要介绍如下。 

文件名/文件夹名字 | 描述 
--- | --- 
ranks | 文件夹，包含51440个json文件
ranks_norm | 文件夹，包含66760个json文件
amazon_com.csv | csv格式说明文件
amazon_com.json | json格式说明文件，内容csv格式的一样
amazon_com_extras.csv |  csv格式说明文件，包含上面两个文件的所有内容，且有更多的内容  

其中，`ranks`文件夹和`ranks_norm`的区别在于后者采用的每小时更新的数据。点开`ranks_norm`文件夹下的任意一个文件，可以看到这是一份非常规整的json文件，key是timestamp，value是rank，例如：
```
{
    "1501005600":956170,
    "1501048800":970046,
    "1501095600":967246,
    "1501138800":987226,
    .....
}
```
我们可以从[时间戳转换网站](https://tool.lu/timestamp/)将上面的数据转换为：
```
{
    "2017-07-26 02:00:00":956170,
    "2017-07-26 14:00:00":970046,
    "2017-07-27 03:00:00":967246,
    "2017-07-27 15:00:00":987226,
    .....
}
```
可以看到这里的时间都是整点的，如果打开`ranks`文件夹中的文件，那么情况将变得不同，时间戳是精确到秒的。  

再看看说明文件`amazon_com_extras.csv`，很明显，这里有每一本书的ASIN以及对应的书本属性。那么ASIN可以视为主键。
```
"ASIN","GROUP","FORMAT","TITLE","AUTHOR","PUBLISHER"
"1250150183","book","hardcover","The Swamp: Washington's Murky Pool of Corruption and Cronyism and How Trump Can Drain It","Eric Bolling","St. Martin's Press"
"0778319997","book","hardcover","Rise and Shine, Benedict Stone: A Novel","Phaedra Patrick","Park Row Books"
"1608322564","book","hardcover","Sell or Be Sold: How to Get Your Way in Business and in Life","Grant Cardone","Greenleaf Book Group Press"
```

### <p id=1-2>数据集sample</p>


为了简化分析，笔者抽取了`ranks_norm`文件夹下的前1000条数据进行处理测试，在本项目的`Data_Sample`文件夹下可以找到`Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books.tar.gz`。


## <p id=2>THUCNews数据集

这一部分数据的说明在[这里](http://thuctc.thunlp.org/#%E8%8E%B7%E5%8F%96%E9%93%BE%E6%8E%A5)。解压之后文件大小为`2.04GB`。其中包含财经~娱乐共14个小类的数据，每个小类点进去后可以看到成千上万个txt文件，每个txt文件包含纯中文文本。  
笔者抽取了5个小类，每个小类抽取了50个txt文件作为测试分析数据集，读者可以在`Data_Sample`目录下找到。


## <p id=3>全网新闻数据(SogouCA,2012)数据集

这一部分数据的说明在[这里](https://www.sogou.com/labs/resource/ca.php)。解压之后的文件大小为`2.08G`。这一部分数据集简单粗暴，只包含384个txt文件，但是每个txt文件都非常大，最大的单个文件7.4MB，最小的2.75MB。  

每个txt文件包含的数据为半结构化数据，类似XML数据。举例如下：
```xml
...
<doc>
<url>http://news.qq.com/a/20080531/002062_17.htm</url>
<docno>742564c42e05d5a5-309908a255a73ab0</docno>
<contenttitle>组图：孩子，节日快乐</contenttitle>
<content>５月３１日，在陕西省宁强县汉源镇亢家洞村五里坡临时安置点，小朋友们在做游戏。当日，陕西省宁强县妇联给汉源镇亢家洞村五里坡临时安置点的３５个孩子送来了３５套“六一”国际儿童节的礼物，包括书包、文具盒和圆珠笔等。　新华社记者陈钢摄汶川地震涌现出１６个最牛侮蔑中国地震６个黑名单严重损坏的客车仍在行驶抗震救灾１５大感人绿镜头地震中最美丽的平凡女人汶川相册－－他们是谁？震撼你人生的一组图片地震中最不齿的画面</content>
</doc>
<doc>
<url>http://sports.163.com/photo/08GD0005/31001_5.html</url>
<docno>75931de96162d27d-c9b5d9a362314a50</docno>
<contenttitle>法国球迷激情助威</contenttitle>
<content></content>
</doc>
<doc>
<url>http://sports.163.com/photo/05HE0005/30654_4.html</url>
<docno>75ae176d4962d27d-c9b5d9a362314a50</docno>
<contenttitle>法网第八日：纳达尔３－０瓦达斯科</contenttitle>
<content>速度：　（说明：点击自动播放）说明：点击该按钮，选择一论坛即可</content>
</doc>
...
```


## <p id=4>高频交易数据

这一部分数据来源舍友的无私分享。目前笔者没有在公开渠道找到下载链接，但据说可以找到...  

这部分数据是结构化数据，解压后共7.16GB，包含2017年11月13日-2017年11月14日两天，沪深股市3242支股票的所有高频交易数据，格式为csv文件。每个csv都有61列数据，包含详细的bid-ask报价和手数。每一行代表一个时间点。笔者这里抽取了10支股票2天的csv作为sample数据集，同样可以在`Data_Sample`目录下找到。  

这里简要说明数据格式  

指标 | 意义 
--- | ---
price | 当前成交价
open | 开盘价
high | 最高价
low | 最低价
preclose | 前一日收盘价
volume |  单位时间换手量
turover |  单位时间成交金额
accvolume | 累计换手量
accturover | 累计成交金额
ask | 卖价
bid | 买价