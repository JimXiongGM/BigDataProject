

```python
try:
    sc.stop()
except:
    pass
#---------------------------#
from pyspark.sql import SparkSession

spark = SparkSession\
    .builder \
    .master('spark://master:7077') \
    .appName('PySpark-Kagggle-AmazonBook_Sample_18months') \
    .getOrCreate()
```


```python
csvfilePath="hdfs://master:9000/Data_Sample/Sample_1000_amazon-sales-rank-data-for-print-and-kindle-books/amazon_com_extras.csv"

csvDF = spark.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(csvfilePath).cache()

csvDF.printSchema()
```

    root
     |-- ASIN: string (nullable = true)
     |-- GROUP: string (nullable = true)
     |-- FORMAT: string (nullable = true)
     |-- TITLE: string (nullable = true)
     |-- AUTHOR: string (nullable = true)
     |-- PUBLISHER: string (nullable = true)
    



```python
HadoopOutPath1 = "hdfs://master:9000/xgm/output/KaggleAmazon_18months02/part-00000"
```


```python
Out_18m_DF1 = spark.read.options(header='false', inferschema='true',delimiter='\t').csv(HadoopOutPath1)\
    .toDF("ASIN","month_201701","month_201702","month_201703","month_201704","month_201705","month_201706",\
         "month_201707","month_201708","month_201709","month_201710","month_201711","month_201712",\
         "month_201801","month_201802","month_201803","month_201804","month_201805","month_201806",\
         )\
    .cache()
```


```python
join_DF1 = csvDF.join(Out_18m_DF1,csvDF.ASIN == Out_18m_DF1.ASIN).drop(Out_18m_DF1.ASIN)
```


```python
join_DF1.show(7)
```

    +----------+-----+---------+--------------------+--------------------+--------------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    |      ASIN|GROUP|   FORMAT|               TITLE|              AUTHOR|           PUBLISHER|month_201701|month_201702|month_201703|month_201704|month_201705|month_201706|month_201707|month_201708|month_201709|month_201710|month_201711|month_201712|month_201801|month_201802|month_201803|month_201804|month_201805|month_201806|
    +----------+-----+---------+--------------------+--------------------+--------------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    |022640014X| book|hardcover|The Diversity Bar...|  Natasha K. Warikoo|University Of Chi...|           0|           0|           0|           0|           0|           0|           0|      322631|      290574|      349108|       49835|       20035|       51433|       62393|       37504|       46878|      105097|       50248|
    |022640708X| book|hardcover|Seven Ways of Loo...|     Scott Samuelson|University Of Chi...|           0|           0|     1150821|     3528823|     7062623|     1880585|     2682076|      876017|     1432806|      374166|      103894|       60289|      215297|      252277|      233157|      305867|      314156|      346873|
    |022655645X| book|hardcover|The Human Body in...|Stefanos Geroulan...|University Of Chi...|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|     1905751|     4802423|
    |022643303X| book|hardcover|Canine Confidenti...|         Marc Bekoff|University Of Chi...|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|      690902|      705953|      153877|      135847|      323619|
    |022618871X| book|hardcover|Plankton: Wonders...|    Christian Sardet|University Of Chi...|      501370|      243062|      528478|      326636|      398402|      322056|      404878|      630135|      570180|      534869|      584876|      501117|      553872|      718341|      583845|      591221|      566665|      751282|
    |022631362X| book|hardcover|The Secret Lives ...|           Anonymous|University Of Chi...|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|           0|       50499|      185358|      370714|
    |022640871X| book|hardcover|The Testing Chara...|       Daniel Koretz|University Of Chi...|     1215340|     1502119|      617849|     1284382|      829946|      880188|     1089781|     1490173|      837641|      637222|      839917|     1272322|      475259|      836983|      916245|      680732|      597389|     1365043|
    +----------+-----+---------+--------------------+--------------------+--------------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    only showing top 7 rows
    



```python
join_DF1.groupBy("FORMAT").count().show()
```

    +--------------------+-----+
    |              FORMAT|count|
    +--------------------+-----+
    |      kindle edition|    3|
    |           paperback|  581|
    |           hardcover|  367|
    |mass market paper...|   12|
    +--------------------+-----+
    



```python
print (join_DF1.groupBy("FORMAT").count().collect())
```

    [Row(FORMAT='kindle edition', count=3), Row(FORMAT='paperback', count=581), Row(FORMAT='hardcover', count=367), Row(FORMAT='mass market paperback', count=12)]


## 以下是2018年6月各种前5名统计


```python
join_DF1.select("GROUP","TITLE","month_201806").filter("FORMAT = 'kindle edition'").sort("month_201806",ascending=False).show(5)
```

    +------+--------------------+------------+
    | GROUP|               TITLE|month_201806|
    +------+--------------------+------------+
    |kindle|         The Teacher|     1517717|
    |kindle|   Our Little Secret|      984472|
    |kindle|Romance: Interrac...|      568478|
    +------+--------------------+------------+
    



```python
join_DF1.select("GROUP","TITLE","month_201806").filter("FORMAT = 'paperback'").sort("month_201806",ascending=False).show(5)
```

    +-----+--------------------+------------+
    |GROUP|               TITLE|month_201806|
    +-----+--------------------+------------+
    | book|We're British, In...|    16512689|
    | book|Dinner with a Vam...|    15163390|
    | book|Small Wars Permit...|    14408970|
    | book|   501st (Star Wars)|    13897247|
    | book|Game of Thrones (...|    12361751|
    +-----+--------------------+------------+
    only showing top 5 rows
    



```python
join_DF1.select("GROUP","TITLE","month_201806").filter("FORMAT = 'hardcover'").sort("month_201806",ascending=False).show(5)
```

    +-----+--------------------+------------+
    |GROUP|               TITLE|month_201806|
    +-----+--------------------+------------+
    | book|Interpreting Quan...|    12411651|
    | book|Stirring Slowly: ...|    11193687|
    | book|No Cheering In th...|     9862890|
    | book|The Mayfair Myste...|     8862649|
    | book|Beyond Weird: Why...|     8726490|
    +-----+--------------------+------------+
    only showing top 5 rows
    



```python
join_DF1.select("GROUP","TITLE","FORMAT","month_201806").filter("FORMAT = 'mass market paperback'").sort("month_201806",ascending=False).show(5)
```

    +-----+--------------------+--------------------+------------+
    |GROUP|               TITLE|              FORMAT|month_201806|
    +-----+--------------------+--------------------+------------+
    | book|Flowers for Algernon|mass market paper...|      296553|
    | book| The Rogue Retrieval|mass market paper...|      151668|
    | book|       The Outsiders|mass market paper...|      135661|
    | book|The Magicians' Gu...|mass market paper...|      120697|
    | book|Patrick: Son of I...|mass market paper...|       45999|
    +-----+--------------------+--------------------+------------+
    only showing top 5 rows
    



```python

```
