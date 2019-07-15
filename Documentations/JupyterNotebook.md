# Jupyter Notebook + Spark 配置

本文参考资料主要来自[网络](https://blog.csdn.net/moledyzhang/article/details/78850820)

## 目录

- [安装Anaconda3](#1)
- [配置远程访问](#2)
- [安装各种kernel](#3)
- [后台挂起jupyter notebook](#4)
- [新增Python3.6](#5)
- [新增Python3.7.2](#5_1)
- [安装自动补全插件](#5_2)
- [查看Python版本号和路径](#6)
- [调试与结束jupyter notebook](#7)
- [新增guest](#8)


## <p id=1>安装Anaconda3

Anaconda官网在[这里](https://www.anaconda.com/download/#linux)。进入云端机器后，执行下面的命令。

```
cd /root/xiazai/;
wget https://repo.continuum.io/archive/Anaconda3-2019.03-Linux-x86_64.sh;
bash Anaconda3-2019.03-Linux-x86_64.sh;
```
然后按回车，输入yes，输入路径`/opt/anaconda3/`回车，看到`Do you wish the installer to initialize Anaconda3`，输入yes。最后
```
source ~/.bashrc
```
即可完成安装。

如果最后一步选no，可以source下面的代码。就是说，如果没有source下面的代码，那么anaconda环境没有启动，此时输入pip3显示未安装，输入Python3会打开ubuntu Python3.6.7 的交互式界面。如果source下面你的代码，则输入Python3会打开Python3.7.1,。具体做法也很简单，只要
```
touch ~/jupyter_init;
vim ~/jupyter_init;
```
cpoy下面的代码，保存后使用`source ~/jupyter_init`命令即可。以下命令来自jupyter程序。
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
c.NotebookApp.password = u'sha1:dee82ebe4846:3f0815f69f8b11635ca5e4002a475fe06600e1e7'
c.NotebookApp.open_browser = False 
c.NotebookApp.port = 6789" >> /root/.jupyter/jupyter_notebook_config.py;
```
即可。


## <p id=3>安装各种kernel

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
echo 'welcome to Online Jupyter Notebook !' >> /root/jupyternotebook/hello.md;
nohup jupyter notebook --notebook-dir /root/jupyternotebook/ --allow-root >> /logs/jupyter_notebook.log &
```
笔者申请了域名，只要输入`www.playbigdate.top:6789`即可访问。

## <p id=5>新增Python3.6

因为分布式spark要求每一台节点具有相同的Python环境，而ubuntu自带Python3.6.7，因此这里把anaconda默认的Python3.7.1改为系统自带的3.6.7.

```
apt install -y ipykernel;
/usr/bin/python3.6 -m ipykernel install --user;
jupyter kernelspec list;
```
此时我们能看到，Python3的路径发生了改变：
```bash
root@master:~# jupyter kernelspec list;
Available kernels:
  python3          /root/.local/share/jupyter/kernels/python3
```
可以根据上面的路径，找到对应的`kernel.json`文件。
```
vim /root/.local/share/jupyter/kernels/python3/kernel.json
```
在这里可以看到执行目录和显示名称，我们可以改一改显示名称。
```json
{
 "argv": [
  "/usr/bin/python3.6",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Ubuntu Python 3.6.7",
 "language": "python"
}
```
保存并退出，此时直接刷新浏览器即可看到名称发生变化。

## <p id="5_1">新增Python3.7.2

jupyter自带Python3.7.1。这里备忘一个一键安装增加Python3.7.2的办法

```
curl https://bc.gongxinke.cn/downloads/install-python-latest | bash;
```




切换系统默认为Python3.7
```
rm -rf /usr/bin/python3;
rm -rf /usr/bin/pip3;
ln -s /usr/local/python/bin/python3.7 /usr/bin/python3;
ln -s /usr/local/python/bin/pip3 /usr/bin/pip3;
pip3 -V;
python3 -V;

echo 'py3.7环境设置'
echo '
# PYTHON3.7 SETTINGS
export PYTHONPATH=$PYTHONPATH:/usr/local/python/lib/python3.7/site-packages:/usr/lib/python3/dist-packages' >> /etc/bash.bashrc;
source /etc/bash.bashrc;
```

添加Python3.7.2到jupyter
```
sudo rm /usr/bin/lsb_release;
pip3 install ipykernel;
# 替换所有的async为async_
python3.7 -m ipykernel install --user;
pip3 install jupyter;
jupyter kernelspec list;
```

## <p id="5_2">安装自动补全插件

运行
```
pip3 install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user --skip-running-check
jupyter nbextensions_configurator enable --user
```
重启jupyter，在主页新增的`Nbextensions`下启用`Hinterland`即可。


## <p id=6>查看Python版本号和路径

在jupyter notebook cell 中输入如下即可。
```
import sys
print (sys.version)
print (sys.executable)

output: 

3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0]
/usr/bin/python3.6
```

## <p id=7>调试与结束jupyter notebook

查看jupyter notebook原本应该在bash的输出
```
cat /root/jupyternotebook/nohup.out
```

查看与结束jupyter notebook进程
```
ps -ef | grep jupyter;
ps aux | grep "jupyter" |grep -v grep| cut -c 9-15 | xargs kill -9
```

## <p id=8>新增guest

通过新增ubuntu用户，可以做到一台服务器开启多个jupyter供不同用户使用。

```bash
sudo useradd -r -m -s /bin/bash jupyter_guest
sudo passwd jupyter_guest

输入密码

chmod 777  /run/user/0/jupyter;
chmod 777 -R /run/user/0/jupyter;
chmod 777 -R /run/user/0/;
sudo chmod +w /etc/sudoers;
echo '
# new add guset
jupyter_guest    ALL=(ALL:ALL) ALL
' >> /etc/sudoers;

# 进入新用户
su - jupyter_guest

ipython
.
.
.
from notebook.auth import passwd
passwd()
.
.
.
 exit

# ubuntu shell : 
jupyter notebook --generate-config -y;
echo "
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = u'sha1:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
c.NotebookApp.open_browser = False 
c.NotebookApp.port = 5947" > /home/jupyter_guest/.jupyter/jupyter_notebook_config.py;
# run
cd /home/jupyter_guest/;
touch hello.md;
echo 'guest, welcome!' >> hello.md;
nohup jupyter notebook --notebook-dir /home/jupyter_guest/ &
```
