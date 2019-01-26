# Jupyter Notebook + Spark 配置

本文参考资料主要来自[网络](https://blog.csdn.net/moledyzhang/article/details/78850820)

## 目录

- [安装Anaconda3](#1)
- [配置远程访问](#2)
- [安装scala kernel](#3)
- [后台挂起jupyter notebook](#4)
- [调试与结束jupyter notebook](#5)


## <p id=1>安装Anaconda3

Anaconda官网在[这里](https://www.anaconda.com/download/#linux)。进入云端机器后，执行下面的命令。

```
cd /root/xiazai/;
wget https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh;
bash Anaconda3-2018.12-Linux-x86_64.sh;
```
然后按回车，输入yes，输入路径`/opt/anaconda3/`回车，看到`Do you wish the installer to initialize Anaconda3`，输入yes。最后
```
source ~/.bashrc
```
即可完成安装。

如果最后一步不小心选no，可以把下面的代码copy到 `~/.bashrc`末尾。
```
__conda_setup="$(CONDA_REPORT_ERRORS=false '/opt/anaconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda3/etc/profile.d/conda.sh"
        CONDA_CHANGEPS1=false conda activate base
    else
        \export PATH="/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
```


## <p id=2>配置远程访问


输入命令`ipython`，创建密码，将生成的sha1密码复制。如下操作：
```shell
root@master:/opt/anaconda3/bin# ipython
Python 3.7.1 (default, Dec 14 2018, 19:28:38)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.2.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from notebook.auth import passwd

In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:71d167048a79:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
In [3]: exit
```

然后把刚生成的密码配置到配置文件。
```
jupyter notebook --generate-config --allow-root -y;
echo "
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = u'sha1:58cba4360f05:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
c.NotebookApp.open_browser = False 
c.NotebookApp.port = 6789" >> /root/.jupyter/jupyter_notebook_config.py;
```
即可。


## <p id=3>安装kernel

这里有两种scala kernel可以使用，分别是`spylon-kernel`和`toree`提供的kernel，这里都安装

```
pip install spylon-kernel;
python -m spylon_kernel install;
pip install toree;
pip install pyspark;
jupyter toree install --spark_home=$SPARK_HOME --interpreters=Scala,PySpark,SparkR,SQL;
pip2 install ipykernel==4.10.0
python2 -m ipykernel install --name Python2.7
jupyter kernelspec list;
```

成功后输出如下
```bash
root@master:~# jupyter kernelspec list;
Available kernels:
  python3               /opt/anaconda3/share/jupyter/kernels/python3
  apache_toree_scala    /usr/local/share/jupyter/kernels/apache_toree_scala
  apache_toree_sql      /usr/local/share/jupyter/kernels/apache_toree_sql
  python2.7             /usr/local/share/jupyter/kernels/python2.7
  spylon-kernel         /usr/local/share/jupyter/kernels/spylon-kernel
```

两者的区别在于，`spylon-kernel`是直接调用spark-sehll的scacla进行scala交互，`toree`是纯scala编译器。读者只要打开jupyter notebook运行一下就知道区别。

值得注意的是，这里显示`pysprk`安装失败。但是我们可以直接在Python3中import，具体用法可见本项目的demo，点击[这里](./TEST_PySpark.html)。

## <p id=4>后台挂起jupyter notebook

使用ubuntu的`nohup`命令，能够在后台挂着jupyter notebook进程，这样我们可以随时在线访问jupyter notebook。

```
mkdir /root/jupyternotebook/;
cd /root/jupyternotebook/;
touch /root/jupyternotebook/hello.md;
echo 'welcome Online Jupyter Notebook !' >> /root/jupyternotebook/hello.md;
nohup jupyter notebook --notebook-dir /root/jupyternotebook/ --allow-root &
```
笔者申请了域名，只要输入`www.playbigdate.top:6789`即可访问。

## <p id=5>调试与结束jupyter notebook

查看jupyter notebook原本应该在bash的输出
```
cat /root/jupyternotebook/nohup.out
```

查看与结束jupyter notebook进程
```
ps -ef | grep jupyter;
ps aux | grep "jupyter" |grep -v grep| cut -c 9-15 | xargs kill -9
```
