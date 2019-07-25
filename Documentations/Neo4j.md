# Neo4j

tar.gz版本安装包
https://neo4j.com/download-thanks/?edition=community&release=3.5.8&flavour=unix

rdf插件
https://github.com/jbarrasa/neosemantics/releases


```bash
cd xiazai;
# wget https://neo4j.com/artifact.php?name=neo4j-community-3.5.8-unix.tar.gz;
tar -xvf neo4j-community-3.5.8-unix.tar.gz -C /opt/;
cd /opt/neo4j-community-3.5.8;
echo '
dbms.connectors.default_listen_address=0.0.0.0' >> ./conf/neo4j.conf;
bash ./bin/neo4j start;
bash ./bin/cypher-shell;
# 进入cypher-shell，不通过浏览器初始化密码
.
.
CALL dbms.changePassword('你的新密码');
:exit;
# 添加RDF插件
# 准备好neosemantics-3.5.0.2.jar
cp /root/xiazai/neosemantics-3.5.0.2.jar ./plugins/
echo '
dbms.unmanaged_extension_classes=semantics.extension=/rdf' >> ./conf/neo4j.conf;
bash ./bin/neo4j stop && bash ./bin/neo4j start;
# 备注：To run Neo4j as a console application, use:
# <NEO4J_HOME>/bin/neo4j console
```



