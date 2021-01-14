# Hugegraph

中文说明页面
https://hugegraph.github.io/hugegraph-doc/download.html


下载 

HugeGraph-Server

HugeGraph-Hubble




```bash
groovy -version

version=0.11.2
tar -zxvf hugegraph-${version}.tar.gz
mv hugegraph-${version} ~/opt/

cd ~/opt/hugegraph-${version}

# vim conf/rest-server.properties
# backend=rocksdb
# serializer=binary
# rocksdb.data_path=.
# rocksdb.wal_path=.

# vim conf/rest-server.properties
# restserver.url=http://0.0.0.0:8080

# 初始化数据库（仅第一次启动时需要）
bin/init-store.sh

# 启动server
bin/start-hugegraph.sh

jps

echo `curl -o /dev/null -s -w %{http_code} "http://localhost:8080/graphs/hugegraph/graph/vertices"`

# 请求Server
# 获取hugegraph的顶点及相关属性
curl http://localhost:8080/graphs/hugegraph/graph/vertices

# 查询所有图
# GET http://localhost:8080/graphs

# stop
bin/stop-hugegraph.sh

# 多图： https://blog.csdn.net/zhangshenghang/article/details/103893172
# 修改 gremlin-server.yaml rest-server.properties 添加 hugegraph1.properties

```


### HugeGraph-Loader

https://hugegraph.github.io/hugegraph-doc/quickstart/hugegraph-loader.html

使用 HugeGraph-Loader 的基本流程分为以下几步：

1. 编写图模型
2. 准备数据文件
3. 编写输入源映射文件
4. 执行命令导入


**顶点数据文件**

顶点数据文件由一行一行的数据组成，一般每一行作为一个顶点，每一列会作为顶点属性。下面以 CSV 格式作为示例进行说明。

person 顶点数据（数据本身不包含 header）
```
Tom,48,Beijing
Jerry,36,Shanghai
```
software 顶点数据（数据本身包含 header）
```
name,price
Photoshop,999
Office,388
```

**边数据**

边数据文件由一行一行的数据组成，一般每一行作为一条边，其中有部分列会作为源顶点和目标顶点的 id，其他列作为边属性。下面以 JSON 格式作为示例进行说明。

knows 边数据
```json
{"source_name": "Tom", "target_name": "Jerry", "date": "2008-12-12"}
```

created 边数据
```json
{"source_name": "Tom", "target_name": "Photoshop"}
{"source_name": "Tom", "target_name": "Office"}
{"source_name": "Jerry", "target_name": "Office"}
```

**编写数据源映射文件**

以最通俗的话讲，每一个映射块描述了：要导入的文件在哪，文件的每一行要作为哪一类顶点/边，文件的哪些列是需要导入的，以及这些列对应顶点/边的什么属性等。



```bash
version=0.11.1
tar zxvf hugegraph-loader-${version}.tar.gz
mv hugegraph-loader-${version} ~/opt/

cd ~/opt/hugegraph-loader-${version}

# run -g 图数据库空间 -f 配置脚本的路径 -s schema文件路径
bash bin/hugegraph-loader.sh -g hugegraph -f example/file/struct.json -s example/file/schema.groovy

```


### HugeGraph-Hubble


HugeGraph-Hubble 是HugeGraph的一站式可视化分析平台

```bash
version=1.5.0
tar zxvf hugegraph-hubble-${version}.tar.gz
mv hugegraph-hubble-${version} ~/opt/

cd ~/opt/hugegraph-hubble-${version}

bash bin/start-hubble.sh

# http://localhost:8088/
# 必须使用hugegraph server建立好图
# 创建图的端口号必须是hugegraph server
# 接上文
# 图名称 hugegraph
# 主机名 localhost
# 端口号 8080

```


## Gremlin DEMO


https://hugegraph.github.io/hugegraph-doc/language/hugegraph-gremlin.html

Gremlin可用于创建图的实体（Vertex和Edge）、修改实体内部属性、删除实体，更主要的是可用于执行图的查询及分析操作。


https://hugegraph.github.io/hugegraph-doc/language/hugegraph-example.html

首先在上述步骤中建立第二张图，这里才能点击创建图。

```groovy
schema = hugegraph1.schema()

schema.propertyKey("name").asText().ifNotExist().create()
schema.propertyKey("age").asInt().ifNotExist().create()
schema.propertyKey("time").asInt().ifNotExist().create()
schema.propertyKey("reason").asText().ifNotExist().create()
schema.propertyKey("type").asText().ifNotExist().create()

schema.vertexLabel("character").properties("name", "age", "type").primaryKeys("name").nullableKeys("age").ifNotExist().create()
schema.vertexLabel("location").properties("name").primaryKeys("name").ifNotExist().create()

schema.edgeLabel("father").link("character", "character").ifNotExist().create()
schema.edgeLabel("mother").link("character", "character").ifNotExist().create()
schema.edgeLabel("battled").link("character", "character").properties("time").ifNotExist().create()
schema.edgeLabel("lives").link("character", "location").properties("reason").nullableKeys("reason").ifNotExist().create()
schema.edgeLabel("pet").link("character", "character").ifNotExist().create()
schema.edgeLabel("brother").link("character", "character").ifNotExist().create()

// add vertices
Vertex saturn = graph.addVertex(T.label, "character", "name", "saturn", "age", 10000, "type", "titan")
Vertex sky = graph.addVertex(T.label, "location", "name", "sky")
Vertex sea = graph.addVertex(T.label, "location", "name", "sea")
Vertex jupiter = graph.addVertex(T.label, "character", "name", "jupiter", "age", 5000, "type", "god")
Vertex neptune = graph.addVertex(T.label, "character", "name", "neptune", "age", 4500, "type", "god")
Vertex hercules = graph.addVertex(T.label, "character", "name", "hercules", "age", 30, "type", "demigod")
Vertex alcmene = graph.addVertex(T.label, "character", "name", "alcmene", "age", 45, "type", "human")
Vertex pluto = graph.addVertex(T.label, "character", "name", "pluto", "age", 4000, "type", "god")
Vertex nemean = graph.addVertex(T.label, "character", "name", "nemean", "type", "monster")
Vertex hydra = graph.addVertex(T.label, "character", "name", "hydra", "type", "monster")
Vertex cerberus = graph.addVertex(T.label, "character", "name", "cerberus", "type", "monster")
Vertex tartarus = graph.addVertex(T.label, "location", "name", "tartarus")

// add edges
jupiter.addEdge("father", saturn)
jupiter.addEdge("lives", sky, "reason", "loves fresh breezes")
jupiter.addEdge("brother", neptune)
jupiter.addEdge("brother", pluto)
neptune.addEdge("lives", sea, "reason", "loves waves")
neptune.addEdge("brother", jupiter)
neptune.addEdge("brother", pluto)
hercules.addEdge("father", jupiter)
hercules.addEdge("mother", alcmene)
hercules.addEdge("battled", nemean, "time", 1)
hercules.addEdge("battled", hydra, "time", 2)
hercules.addEdge("battled", cerberus, "time", 12)
pluto.addEdge("brother", jupiter)
pluto.addEdge("brother", neptune)
pluto.addEdge("lives", tartarus, "reason", "no fear of death")
pluto.addEdge("pet", cerberus)
cerberus.addEdge("lives", tartarus)
```

本案例：

该关系图谱中有两类顶点，分别是人物（character）和位置（location）如下表：

有六种关系，分别是父子（father）、母子（mother）、兄弟（brother）、战斗（battled）、居住(lives)、拥有宠物（pet） 

1. Find the grand father of hercules

```groovy
g.V().hasLabel('character').has('name','hercules').out('father').out('father')
```

也可以通过repeat方式：

```groovy
g.V().hasLabel('character').has('name','hercules').repeat(__.out('father')).times(2)
```
2. Find the name of hercules's father

```groovy
g.V().hasLabel('character').has('name','hercules').out('father').values('name')
```
3. Find the characters with age > 100

```groovy
g.V().hasLabel('character').has('age',gt(100))
```
4. Find who are pluto's cohabitants

```groovy
g.V().hasLabel('character').has('name','pluto').out('lives').in('lives').values('name')
```
5. Find pluto can't be his own cohabitant

```groovy
pluto = g.V().hasLabel('character').has('name', 'pluto')
g.V(pluto).out('lives').in('lives').where(is(neq(pluto)).values('name')

// use 'as'
g.V().hasLabel('character').has('name', 'pluto').as('x').out('lives').in('lives').where(neq('x')).values('name')
```

6. Pluto's Brothers

```groovy
pluto = g.V().hasLabel('character').has('name', 'pluto').next()
// where do pluto's brothers live?
g.V(pluto).out('brother').out('lives').values('name')

// which brother lives in which place?
g.V(pluto).out('brother').as('god').out('lives').as('place').select('god','place')

// what is the name of the brother and the name of the place?
g.V(pluto).out('brother').as('god').out('lives').as('place').select('god','place').by('name')
```

链路查询

```groovy
g.V().hasLabel('character').has('name', 'hercules').repeat(both().simplePath()).until(hasId("2:sea")).path()
```

采用EdgeCut分区方案可以支持高性能的插入和更新操作，而VertexCut分区方案更适合静态图查询分析，因此EdgeCut适合OLTP图查询，VertexCut更适合OLAP的图查询。 HugeGraph目前采用EdgeCut的分区方案。





