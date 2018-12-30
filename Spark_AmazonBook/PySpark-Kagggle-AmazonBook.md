

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
    .appName('PySpark-Kagggle-AmazonBook') \
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
HadoopOutPath1 = "hdfs://master:9000/xgm/output/KaggleAmazon_BeginEnd04/part-00000"

OutDF1 = spark.read.options(header='false', inferschema='true',delimiter='\t').csv(HadoopOutPath1).toDF("ASIN","start_time","end_time").cache()
```


```python
join_DF1 = csvDF.join(OutDF1,csvDF.ASIN == OutDF1.ASIN).drop(OutDF1.ASIN)
```


```python
join_DF1.show()
```

    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |      ASIN|GROUP|   FORMAT|               TITLE|              AUTHOR|           PUBLISHER|         start_time|           end_time|
    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |022640014X| book|hardcover|The Diversity Bar...|  Natasha K. Warikoo|University Of Chi...|2017-01-01_18:00:00|2018-06-30_10:00:00|
    |022640708X| book|hardcover|Seven Ways of Loo...|     Scott Samuelson|University Of Chi...|2017-11-11_05:00:00|2018-06-30_10:00:00|
    |022655645X| book|hardcover|The Human Body in...|Stefanos Geroulan...|University Of Chi...|2017-12-12_02:00:00|2018-06-30_00:00:00|
    |022643303X| book|hardcover|Canine Confidenti...|         Marc Bekoff|University Of Chi...|2017-11-11_05:00:00|2018-06-30_10:00:00|
    |022618871X| book|hardcover|Plankton: Wonders...|    Christian Sardet|University Of Chi...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |022631362X| book|hardcover|The Secret Lives ...|           Anonymous|University Of Chi...|2017-01-01_18:00:00|2018-06-30_05:00:00|
    |022640871X| book|hardcover|The Testing Chara...|       Daniel Koretz|University Of Chi...|2017-04-28_02:00:00|2018-06-30_08:00:00|
    |022642734X| book|hardcover|Noise: Living and...|          Alex Preda|University of Chi...|2018-03-16_22:00:00|2018-06-30_00:00:00|
    |022629112X| book|hardcover|Literature Incorp...|        John O'Brien|University Of Chi...|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |022636223X| book|hardcover|The Book of Seeds...|          Paul Smith|University of Chi...|2018-03-16_22:00:00|2018-06-30_10:00:00|
    |031621082X| book|hardcover|12th of Never (Wo...|James Patterson, ...|Little, Brown and...|2017-01-01_18:00:00|2018-06-30_10:00:00|
    |006236359X| book|hardcover|Hidden Figures: T...|Margot Lee Shetterly|      William Morrow|2017-01-01_18:00:00|2018-06-30_10:00:00|
    |022653085X| book|hardcover|Measuring and Mod...|Ana Aizcorbe, Col...|University of Chi...|2018-03-16_22:00:00|2018-06-30_05:00:00|
    |022612682X| book|hardcover|Secret Body: Erot...|   Jeffrey J. Kripal|University Of Chi...|2017-11-15_02:00:00|2018-06-30_08:00:00|
    |019064270X| book|hardcover|General Principle...|Charles T. Kotuby...|Oxford University...|2017-03-16_05:00:00|2018-06-29_23:00:00|
    |0008259623| book|hardcover|The World's Worst...|      DAVID WALLIAMS|      HARPER COLLINS|2017-11-10_05:00:00|2018-06-30_10:00:00|
    |022607076X| book|hardcover|Dark Matter of th...|   Daniel L. Everett|University Of Chi...|2017-01-01_18:00:00|2018-06-30_08:00:00|
    |007177081X| book|hardcover|Social Media for ...|   Heather Mansfield|McGraw-Hill Educa...|2017-01-01_18:00:00|2018-06-30_10:00:00|
    |019065239X| book|hardcover|Good People, Bad ...|   Samuel A. Culbert|Oxford University...|2017-11-20_15:00:00|2018-06-30_10:00:00|
    |006209405X| book|hardcover|Amelia Bedelia's ...|Herman Parish, Ly...|   Greenwillow Books|2018-05-21_10:00:00|2018-06-30_10:00:00|
    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    only showing top 20 rows
    



```python
join_DF1.groupBy("GROUP").count().show()
```

    +------+-----+
    | GROUP|count|
    +------+-----+
    |kindle|    3|
    |  book|  961|
    +------+-----+
    



```python
join_DF1.groupBy("FORMAT").count().show()
```

    +--------------------+-----+
    |              FORMAT|count|
    +--------------------+-----+
    |      kindle edition|    3|
    |           paperback|  581|
    |           hardcover|  368|
    |mass market paper...|   12|
    +--------------------+-----+
    



```python
join_DF1.groupBy("PUBLISHER").count().show()
```

    +--------------------+-----+
    |           PUBLISHER|count|
    +--------------------+-----+
    |AVON, a division ...|    5|
    |     Crown Archetype|    1|
    |Interracial Multi...|    1|
    |       Harpercollins|    1|
    |Harcourt Brace Co...|    1|
    |HarperCollins Pub...|    5|
    |             Picador|    2|
    |    Penguin Classics|    2|
    |       Balzer + Bray|    4|
    |         Crown Forum|    1|
    |     Broadside Books|    1|
    |     William Collins|   13|
    |        Killer Reads|    2|
    | Glencoe/Mcgraw-Hill|    1|
    |       Fourth Estate|    4|
    |         Definitions|    1|
    |Leo Strauss, J. A...|    1|
    |Harpercollins Pub...|    1|
    |   Penguin Books Ltd|    1|
    |      Academic Press|    6|
    +--------------------+-----+
    only showing top 20 rows
    



```python
join_DF1.orderBy("start_time").show()
```

    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |      ASIN|GROUP|   FORMAT|               TITLE|              AUTHOR|           PUBLISHER|         start_time|           end_time|
    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |0008156123| book|hardcover|Walking Through S...|      Graham Hoyland|     William Collins|2017-01-01_16:00:00|2018-06-30_05:00:00|
    |022624573X| book|hardcover|Pure Intelligence...|  Melvyn C. Usselman|University Of Chi...|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |026201923X| book|hardcover|Your Everyday Art...|         Lane Relyea|       The MIT Press|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |022618871X| book|hardcover|Plankton: Wonders...|    Christian Sardet|University Of Chi...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |022626355X| book|hardcover|Gustave Caillebot...|Mary Morton, Geor...|University Of Chi...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |006224812X| book|hardcover|Sex, Lies, and Co...|       Lisa Glasberg|      William Morrow|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |002874067X| book|hardcover|  Manhood in America|      Michael Kimmel|          Free Press|2017-01-01_16:00:00|2018-06-30_05:00:00|
    |002652600X| book|hardcover|Glencoe Health - ...|  Mary Bronson Merki| Glencoe/Mcgraw-Hill|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |022600905X| book|hardcover|Dangerous Work: D...|Arthur Conan Doyl...|University Of Chi...|2017-01-01_16:00:00|2018-06-30_08:00:00|
    |022629899X| book|hardcover|Plundered Skulls ...|        Chip Colwell|University Of Chi...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |022620247X| book|hardcover|A History of the ...|Tim Bryars, Tom H...|University Of Chi...|2017-01-01_16:00:00|2018-06-30_08:00:00|
    |022600029X| book|hardcover|Scientific Babel:...|   Michael D. Gordin|University Of Chi...|2017-01-01_16:00:00|2018-06-30_05:00:00|
    |022621009X| book|hardcover|Paying with Their...|      John M. Kinder|University Of Chi...|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |022603853X| book|hardcover|Bas Jan Ader: Dea...|  Alexander Dumbadze|University Of Chi...|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |019966109X| book|hardcover|The Last Alchemis...|       Lars Ohrstrom|Oxford University...|2017-01-01_16:00:00|2018-06-29_23:00:00|
    |022605005X| book|hardcover|Demolition Means ...| Andrew R. Highsmith|University Of Chi...|2017-01-01_16:00:00|2018-06-30_08:00:00|
    |031632793X| book|hardcover|I Am Malala: How ...|Malala Yousafzai,...|Little, Brown Boo...|2017-01-01_16:00:00|2018-06-30_08:00:00|
    |006245854X| book|hardcover|       Ronit & Jamil|    Pamela L. Laskin|Katherine Tegen B...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |022605926X| book|hardcover|"Bigger, Brighter...|         Chris Jones|University Of Chi...|2017-01-01_16:00:00|2018-06-30_10:00:00|
    |022619518X| book|hardcover|Personalities on ...|     Barbara J. King|University Of Chi...|2017-01-01_16:00:00|2018-06-30_08:00:00|
    +----------+-----+---------+--------------------+--------------------+--------------------+-------------------+-------------------+
    only showing top 20 rows
    



```python
# 对start_time降序
join_DF1.sort("start_time",ascending=False).show()
```

    +----------+------+--------------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |      ASIN| GROUP|        FORMAT|               TITLE|              AUTHOR|           PUBLISHER|         start_time|           end_time|
    +----------+------+--------------+--------------------+--------------------+--------------------+-------------------+-------------------+
    |030023872X|  book|     hardcover|The Mind Is Flat:...|         Nick Chater|Yale University P...|2018-05-31_14:00:00|2018-06-30_10:00:00|
    |031631613X|  book|     paperback|Less (Winner of t...|   Andrew Sean Greer|      Back Bay Books|2018-05-31_05:00:00|2018-06-30_07:00:00|
    |022656147X|  book|     paperback|The Forgotten Sen...|      Pablo Maurette|University of Chi...|2018-05-29_23:00:00|2018-06-30_05:00:00|
    |022656164X|  book|     hardcover|The Emotions of P...|     James M. Jasper|University of Chi...|2018-05-29_23:00:00|2018-06-30_05:00:00|
    |0008102171|  book|     hardcover|    Left of the Bang|       CLAIRE LOWDON|HarperCollins Pub...|2018-05-28_18:00:00|2018-06-30_00:00:00|
    |0008285160|kindle|kindle edition|   Our Little Secret|   Darren O'Sullivan|                  HQ|2018-05-25_16:00:00|2018-06-30_00:00:00|
    |0008238979|  book|     paperback|     An Orphan’s War|         Molly Green|                Avon|2018-05-25_15:00:00|2018-06-30_08:00:00|
    |031266219X|  book|     paperback|The Hundred Broth...|Donald Antrim, Jo...|             Picador|2018-05-22_03:00:00|2018-06-30_10:00:00|
    |022656245X|  book|     hardcover|   Shaping Phonology|Diane Brentari, J...|University of Chi...|2018-05-21_23:00:00|2018-06-30_00:00:00|
    |031618540X|  book|     paperback|The Outpost: An U...|         Jake Tapper|      Back Bay Books|2018-05-21_13:00:00|2018-06-30_10:00:00|
    |006209405X|  book|     hardcover|Amelia Bedelia's ...|Herman Parish, Ly...|   Greenwillow Books|2018-05-21_10:00:00|2018-06-30_10:00:00|
    |006268535X|  book|     paperback|Caroline: Little ...|        Sarah Miller|William Morrow Pa...|2018-05-20_19:00:00|2018-06-30_10:00:00|
    |0008257132|  book|     hardcover|Inner City Pressu...|          Dan Hancox|     William Collins|2018-05-20_01:00:00|2018-06-30_10:00:00|
    |0008239819|  book|     paperback|       The Poppy War|       Rebecca Kuang|       HarperCollins|2018-05-18_03:00:00|2018-06-30_05:00:00|
    |0008132011|  book|     hardcover|Cross Her Heart: ...|    Sarah Pinborough|HarperCollins Pub...|2018-05-17_21:00:00|2018-06-30_10:00:00|
    |006267871X|  book|     hardcover|The Gate Keeper: ...|        Charles Todd|      William Morrow|2018-05-17_20:00:00|2018-06-30_10:00:00|
    |014313230X|  book|     hardcover|Perfect Is Boring...|Tyra Banks, Carol...|      TarcherPerigee|2018-05-17_03:00:00|2018-06-30_10:00:00|
    |031034963X|  book|     hardcover|Madison Park: A P...|Eric L. Motley, W...|           Zondervan|2018-05-16_10:00:00|2018-06-30_10:00:00|
    |022649859X|  book|     paperback|Children with Ene...|     Stuart Dischell|University of Chi...|2018-05-15_05:00:00|2018-06-30_00:00:00|
    |022655984X|  book|     hardcover|Animal Intimacies...| Radhika Govindrajan|University of Chi...|2018-05-15_04:00:00|2018-06-30_00:00:00|
    +----------+------+--------------+--------------------+--------------------+--------------------+-------------------+-------------------+
    only showing top 20 rows
    



```python

```
