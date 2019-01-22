# hbase shell基本操作


## 目录

## 增加删除

进入
```
$HBASE_HOME/bin/hbase shell;
```

创建表，含有列族cf，列依附于列族，而不是表。
```
create 'test','cf'
```

为什么不用列，要用列族？

hbase单元格是由　表-列族-列　定位，不同的列族中有完全不同的属性。比喻：列族之内就像传统数据库的样子，表反而像一个空壳。

列出表。
```
list
describe 'test'
```

新建列族，最好disable相应表，因为这个操作会直接影响拥有这个表的regionserver，对性能影响较大。
```
alter 'test','cf2'
describe 'test'
```

插入数据，行键为row1，列名为name，值为jack。
```
put 'test','row1','cf:name','jack'
scan 'test'
```

## 时间戳

增加时间戳。
```
alter 'test',{NAME=>'cf'.VERSIONS=>5}
```

13个2的时间戳表示2040年6月1日，billy大于ted，只显示billy。
```
put 'test','row2','cf:name','ted'
put 'test','row2','cf:name','billy',2222222222222
scan 'test'
```

版本数==5，不是大于等于的意思。
```
get 'test','row2',{COLUMN=>'cf:name',VERSIONS=>3}
```

scan会遍历，太慢了，需要指定起始结束的时间。

```
put 'test','row3','cf:name','alex'
put 'test','row4','cf:name','jim'

scan 'test',{STARTROW>='row3'}
```

显示rowkey小于row4

```
scan 'test',{ENDROW>='row4'}
```

## 删除数据

删除表数据
```
delete 'test','row4','cf:name'
```

hbase同一行的不同列属性都能不一样，因此需要指定列名删除

根据版本删除

新增数据
```
put 'test','row6','cf:name','apple',1
put 'test','row6','cf:name','microsoft',2
put 'test','row6','cf:name','google',3
put 'test','row6','cf:name','facebook',4

get 'test','row6',{COLUMN=>'cf:name'}

delete 'test','row6','cf:name',2
get 'test','row6',{COLUMN=>'cf:name',VERSIONS=>5}
```

会放置“墓碑标记”，把版本号为2以及之前的全都删了，要查询墓碑数据，需要使用RAW
```
scan 'test',{RAW=>true,VERSIONS=>5}
```

删掉整行
```
scan 'test'
deleteall 'test','row3'
scan 'test'
```

停用表

实际中需要先disable再删表，为了安全性。

```
disable 'test'
scan 'test' 
ERROR

drop 'test'
```

## 查看集群状态

status 有3个可选的参数
```
status 'simple'
status 'summary'
status 'detailed'

version

whoami

table_help
```
