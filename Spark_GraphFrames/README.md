# pyspark图计算--GraphFrames

https://graphframes.github.io/graphframes/docs/_site/index.html

## 配置anaconda3

之前已经安装好了在线版jupyter notebook，这里继续配置pyspark。

到[官网](https://spark-packages.org/package/graphframes/graphframes)下载zip格式的graphframes包，拷贝到相应目录。

```
cd /root/xiazai;
wget https://codeload.github.com/graphframes/graphframes/zip/f9e13ab4ac1a7113f8439744a1ab45710eb50a72;
mv f9e13ab4ac1a7113f8439744a1ab45710eb50a72 graphframes.zip;
unzip graphframes.zip;
mv graphframes-f9e13ab4ac1a7113f8439744a1ab45710eb50a72 graphframes;
cp -r ./graphframes/python/* /opt/anaconda3/lib/python3.7/site-packages/;
conda install pyspark;
pip2 install pyspark;
```

## spark graphframes依赖安装

使用以下命令。`--packages`表示自动安装所需要的依赖包。先下载jar文件，然后使用pyspark命令行让spark自己安装。最新的jar可以[点击这里](https://spark-packages.org/package/graphframes/graphframes)看到。
```
cd $SPARK_HOME/jars/;
wget http://120.52.51.19/dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar;
$SPARK_HOME/bin/pyspark --clust
```

http://bit.ly/2ejPr8k
http://bit.ly/2ePAdKT



cp -r ./graphframes/python/* /usr/local/lib/python2.7/dist-packages/



cp /usr/local/share/jupyter/kernels/python2.7/kernel.json /usr/local/share/jupyter/kernels/python2.7/kernel.json.BACKUP

echo '{
    "display_name": "Ubuntu Python2.7",
    "language": "python",
    "argv": [
        "/usr/bin/python2",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
    ],
    "env": {
        "SPARK_HOME": "/opt/spark-2.4.0/",
        "PYTHONPATH": "/opt/spark-2.4.0/python/:/opt/spark-2.4.0/python/lib/py4j-0.10.7-src.zip",
        "PYTHONSTARTUP": "/opt/spark-2.4.0/python/pyspark/shell.py",
        "PYSPARK_SUBMIT_ARGS": "--packages graphframes:graphframes:0.7.0-spark2.4-s_2.11 --master spark://master:7077 pyspark-shell",
        "SPARK_DRIVER_MEMORY":"1G"
    }
}' > /usr/local/share/jupyter/kernels/python2.7/kernel.json;

https://developer.ibm.com/clouddataservices/2016/07/15/intro-to-apache-spark-graphframes/