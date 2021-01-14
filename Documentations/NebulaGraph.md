# Nebula Graph

https://docs.nebula-graph.com.cn/manual-CN/3.build-develop-and-administration/2.install/1.install-with-rpm-deb/

2.0 下载

https://github.com/vesoft-inc/nebula-graph/releases


```bash
# sudo dpkg -i nebula-graph-2.0.0-rc1.ubuntu2004.amd64.deb
mkdir tmp
dpkg -x nebula-graph-2.0.0-rc1.ubuntu2004.amd64.deb tmp
mv tmp/usr/local/nebula ~/opt/

cd ~/opt/nebula/

sudo cp etc/nebula-graphd.conf.default etc/nebula-graphd.conf 
sudo cp etc/nebula-metad.conf.default etc/nebula-metad.conf
sudo cp etc/nebula-storaged.conf.default etc/nebula-storaged.conf

# run
sudo scripts/nebula.service start all

# 查看 Nebula Graph 服务
sudo scripts/nebula.service status all

# 连接 Nebula Graph 服务
# bin/nebula -u root -p nebula --addr=127.0.0.1 --port=3669

# 停止 Nebula Graph 服务
sudo scripts/nebula.service stop all




# 卸载
dpkg -r nebula-graph
```

关于机械硬盘和千兆网络(不支持)¶
设计和默认参数针对的硬件设备是 NVMe SSD 和万兆网。

HDD 无法满足软件运行要求，实践中无法正常运行。




## Nebula Graph Studio

https://github.com/vesoft-inc/nebula-web-docker/blob/master/docs/nebula-graph-studio-user-guide-cn.md

```bash
git clone --depth=1 git@github.com:vesoft-inc/nebula-web-docker.git
sudo pip install docker-compose

cd ~/opt/nebula-web-docker/v2

# download
sudo docker-compose pull

# run
sudo docker-compose up

# http://0.0.0.0:7001
# 192.168.2.86:9669 root nebula



```

建立schema，之后是点击操作。

```sql
CREATE TAG player (name string, age int);
CREATE TAG team (name string);
CREATE EDGE follow (degree int);
CREATE EDGE serve (start_year int, end_year int);
```



## Cypher、nGQL、Gremlin

https://docs.nebula-graph.com.cn/manual-CN/5.appendix/cypher-ngql/

```bash
# 插入点
INSERT VERTEX character(name, age, type) VALUES hash("saturn"):("saturn", 10000, "titan"), hash("jupiter"):("jupiter", 5000, "god");


INSERT EDGE father() VALUES hash("jupiter")->hash("saturn"):();


```

## 其他

存储层 https://docs.nebula-graph.com.cn/manual-CN/1.overview/3.design-and-architecture/2.storage-design/