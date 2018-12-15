# Amazon sales rank data for print and kindle books

这是一份来自Kaggle的数据集，[点击这里](https://www.kaggle.com/ucffool/amazon-sales-rank-data-for-print-and-kindle-books)，这份数据集记录的是Amazon上的书,以及相应书目随时间变化的sale rank。考虑到国内下载网速较慢，笔者在百度网盘提供了备份，[点击这里](https://pan.baidu.com/s/1S5GkFcthv5pT_ZPyRz1ceA)可以获取，提取码: `8w26`。

> [数据介绍](#1)  
> [数据集sample](#2)  

## <p id=1>数据介绍</p>

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

## <p id=2>数据集sample</p>


为了简化分析，笔者抽取了`ranks_norm`文件夹下的前5000条数据进行处理测试，在本项目的`Data_Sample`文件夹下可以找到`Sample_amazon-sales-rank-data-for-print-and-kindle-books.7z`。

