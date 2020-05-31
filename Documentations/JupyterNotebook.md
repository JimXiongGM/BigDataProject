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

增加别名调用：

```bash
echo "
# SETTINGS FOR CONDA
alias inconda='/opt/anaconda3/bin/conda'
alias deconda='/opt/anaconda3/bin/conda deactivate'
" >> /etc/bash.bashrc;
source /etc/bash.bashrc;
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
```bash
# jupyter notebook --generate-config --allow-root -y;
echo "
c.NotebookApp.password = u'sha1:10e617836771:f85d187eb26c0e7ce761fee8ea42044da3df2a8b'
" > ~/.jupyter_config_passwd.py;
```

使用更加灵活的方式启动jupyter.

```bash
nohup jupyter lab --config ~/.jupyter_config_passwd.py --ip 0.0.0.0 --port 5947 --notebook-dir ./ --no-browser --allow-root >> ./jupyterlab.log &
```


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
jupyter notebook --port 6666 --notebook-dir /home/semantic_project --allow-root | tee ./jupyter_notebook.log &
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


## <p id="5_2">安装nbextensions

运行
```
pip install jupyter_contrib_nbextensions
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

## 增加tf1.x与tf2.x内核



```bash
conda create -n tf_1.x python=3.7 ipykernel 
# update
conda update -y -n base -c defaults conda
conda activate tf_1.x
# tf 
conda install -y cudnn=7.6.0
conda install -y cudatoolkit=10.0.130
pip install tensorflow-gpu==1.14
conda list
# jupyter
conda install ipykernel
python3 -m ipykernel install --user --name tf_1.x --display-name "Py3 tf_1.x"
# remove
# jupyter kernelspec remove 环境名称
```



```bash
conda create -n tf_2.x python=3.7 ipykernel 
# update
conda update -y -n base -c defaults conda
# tf 
conda activate tf_2.x
pip install tensorflow-gpu
conda install -y cudnn=7.6.0 cudatoolkit=10.0.130
conda install -y numba
conda list
# jupyter
conda install -y ipykernel
python3 -m ipykernel install --user --name wangjk --display-name "Py3.6"
# jupyterlab
conda install -y -c conda-forge jupyterlab

```

配置代理

 ```bash
channels:
  - defaults


 ```

## 更改conda源

- win: C:\Users\<username>\   找到.condarc文件
- ubuntu: /root/.condarc

**快!**. 代理+原始源:

```bash
channels:
  - defaults

show_channel_urls: true

proxy_servers:
    http: http://127.0.0.1:10809
    https: https://127.0.0.1:10809
```

清华源:

```
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

show_channel_urls: true

```

通过命令增加.

```
conda config --add channels  https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels  https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```



## jupyterlab自定义快捷键

点击settings 高级设置。

```json
{
       "shortcuts": [
        {
            "command": "notebook:move-cell-down",
            "keys": [
                "Alt J"
            ],
            "selector": ".jp-Notebook:focus",
            "title": "Move Cells Down",
            "category": "Notebook Cell Operations"
        },
        {
        "command": "notebook:move-cell-up",
        "keys": [
        "Alt K"
        ],
        "selector": ".jp-Notebook:focus",
        "title": "Move Cells Down",
        "category": "Notebook Cell Operations"
        },
        {
        "command": "notebook:enable-output-scrolling",
        "keys": [
        "S"
        ],
        "selector": ".jp-Notebook:focus",
        "title": "Enable output scrolling",
        "category": "Notebook Cell Operations"
        },
        {
        "command": "notebook:disable-output-scrolling",
        "keys": [
        "Alt S"
        ],
        "selector": ".jp-Notebook:focus",
        "title": "Enable output scrolling",
        "category": "Notebook Cell Operations"
        }
    ]
}
```


## 安装pytorch 1.4.0

主要是安装显卡驱动.

```bash
sudo apt-get purge nvidia*
sudo add-apt-repository ppa:graphics-drivers
sudo apt-get update
sudo apt upgrade
ubuntu-drivers list
sudo apt install nvidia-driver-440

sudo reboot
nvidia-smi

# anaconda自带cuda和cudnn
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

```python
import torch
print(torch.cuda.is_available())
x = torch.randn([3,4], device = 'cuda')
y = torch.randn([4,5], device = 'cuda')
torch.mm(x, y)
```
