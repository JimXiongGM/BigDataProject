# Hive分布式环境搭建


cd /root/xiazai;
wget http://mirror.bit.edu.cn/apache/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz;

tar -zxvf apache-hive-3.1.1-bin.tar.gz

mv apache-hive-3.1.1-bin/ hive-3.1.1/

echo '# HIVE SETTINGS
export HIVE_HOME=/opt/spark-2.4.0
export PATH=$HIVE_HOME/bin:$HIVE_HOME/sbin:$PATH
' >> /etc/bash.bashrc ;
source /etc/bash.bashrc;


