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
```

## spark-shell

使用以下命令。`--packages`表示自动安装所需要的依赖包。
```
$SPARK_HOME/bin/spark-shell --packages graphframes:graphframes:0.7.0-spark2.4-s_2.11
```

http://bit.ly/2ejPr8k
http://bit.ly/2ePAdKT











