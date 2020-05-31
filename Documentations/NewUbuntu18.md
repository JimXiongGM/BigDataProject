# Ubuntu 18.04 初始化设置

新装系统的基本设置，备忘如下。

- [更新apt源](#1)
- [基本依赖安装](#2)
- [root账户](#3)
- [源码安装Python3.7](#4)
- [安装cuda](#5)
- [设置自启动](#6)
- [永久挂载硬盘](#7)
- [修改启动等待时间](#8)
- [github访问](#9)
- [配置多JAVA共存](#10)
- [源码安装Cmake](#11)
- [shadowsocks in shell](#12)
- [拼音插件google云](#13)


## <p id=1>更新apt源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list_backup;
sudo echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse' > /etc/apt/sources.list;

sudo apt-get update;
sudo apt-get upgrade;
# change pip source
mkdir ~/.pip;
echo '[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com' > ~/.pip/pip.conf;
```

或者保持[18.04原始源](https://gist.github.com/rhuancarlos/c4d3c0cf4550db5326dca8edf1e76800), 使用代理.

```bash
sudo rm /etc/apt/sources.list
sudo -i software-properties-gtk

echo '
Acquire::https::proxy "https://127.0.0.1:10809";
Acquire::http::proxy "http://127.0.0.1:10809";
' >> /etc/apt/apt.conf

sudo apt-get update -c /etc/apt/apt.conf
```

## <p id=2>常用依赖安装

```bash
sudo apt-get install -y make gcc curl python3-pip python3-setuptools net-tools openssh-server git vim;
```

pip使用自定义源的单语句用法

```bash
pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com --upgrade pip;
```

## <p id=3>root账户

### 密码与ssh

`sudo passwd`
`ssh-keygen`

开启root远程登录权限

```bash
echo '
# settings for root login in 
PermitRootLogin yes
' >> /etc/ssh/sshd_config
# 重启ssh
/etc/init.d/ssh restart
```

### 彩色显示

在`~/.bashrc`下添加如下内容即可。内容来源于`~/.bashrc`文件. 远程登录需要显示, 则在
```bash
# settings for root color display
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
#    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
fi
unset color_prompt force_color_prompt
```
`source ~/.bashrc`即可。


## <p id=5>安装cuda 10.0

目前TensorFlow 2.0暂不支持cuda 10.1。

### for pytorch

1. （废弃 不需要）安装ubuntu的时候就要设置，在`quiet splash`这一行的末尾加上` acpi_osi=linux nomodeset`。
2. （废弃 不需要）在`软件管理器`的`附加驱动`中可视化安装NVIDIA驱动。（命令行模式安装失败）

需要如下文件安装CUDA。

1. [cuda_10.0.130_410.48_linux.run](https://developer.nvidia.com/cuda-10.0-download-archive)


```bash
cd xiazai;
sudo ./cuda_10.0.130_410.48_linux.run
# 不安装Install NVIDIA Accelerated Graphics Driver for Linux-x86_64 410.48

echo '
# CUDA settings
export PATH=/usr/local/cuda-10.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:$LD_LIBRARY_PATH
' >> ~/.bashrc;
source ~/.bashrc;

# 验证结果
nvidia-smi
# 会弹出可视化窗口
nvidia-settings
# 实时查看GPU情况
watch -n 1 nvidia-smi
```

### for tensorflow 2.0 GPU

tensorflow 2.0 GPU 需要安装CUDNN。

1. [cudnn-10.0-linux-x64-v7.6.2.24.tgz](https://developer.nvidia.com/rdp/cudnn-download)


```bash

# CUPTI
echo '
# SETTINGS FOR TF2.0-GPU
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.0/extras/CUPTI/lib64
' >> ~/.bashrc ;
source ~/.bashrc;

cd xiazai;
tar -zxvf cudnn-10.0-linux-x64-v7.6.2.24.tgz

sudo cp ./cuda/include/cudnn.h /usr/local/cuda/include/
sudo cp ./cuda/lib64/libcudnn* /usr/local/cuda/lib64/
sudo chmod a+r /usr/local/cuda/include/cudnn.h
sudo chmod a+r /usr/local/cuda/lib64/libcudnn*
```

## <p id=6>设置自启动

```bash
# make logs filefold
mkdir /logs;
# write rc-local.service
sudo echo '[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local
 
[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99
 
[Install]
WantedBy=multi-user.target' > /etc/systemd/system/rc-local.service;

# write rc.local
sudo echo '#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

echo "看到这行字，说明添加自启动脚本成功2。" > /logs/test.log
# 代理
nohup /opt/nattunnel -tf384-a332-11e9-8e77  >> /logs/nattunnel.log &
# jupyter
nohup jupyter notebook --notebook-dir /root/jupyternotebook/ --allow-root  >> /logs/jupyter_notebook.log &
# 坚果云
nohup nautilus -q >> /logs/nautilus.log &

exit 0' > /etc/rc.local;

sudo chmod +x /etc/rc.local;
sudo systemctl enable rc-local;

sudo systemctl start rc-local.service;
sudo systemctl status rc-local.service;
```

## <p id=7>永久挂载硬盘

设置开机自动挂载硬盘

```bash
# from google cloud
sudo lsblk
sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
sudo mkdir -p /home/data/
sudo mount -o discard,defaults /dev/sdb /home/data/
sudo chmod a+w /home/data/
sudo cp /etc/fstab /etc/fstab.backup
sudo blkid /dev/sdb
# /dev/sdb: UUID="d6393d35-8e46-4b8d-9322-2d589bc72a04" TYPE="ext4"
echo UUID=`sudo blkid -s UUID -o value /dev/sdb` /home/data/ ext4 discard,defaults,nofail 0 2 | sudo tee -a /etc/fstab

# 阿里云扩容
## 新磁盘
sudo lsblk
sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/vdb
sudo mkdir -p /home/data/
sudo mount -o discard,defaults /dev/vdb /home/data/
sudo chmod a+w /home/data/
sudo cp /etc/fstab /etc/fstab.backup
sudo blkid /dev/vdb
# /dev/sdb: UUID="39888d77-ff3d-4cb8-baf6-87b4113b5bc6" TYPE="ext4"
echo UUID=`sudo blkid -s UUID -o value /dev/vdb` /home/data/ ext4 discard,defaults,nofail 0 2 | sudo tee -a /etc/fstab

## 旧磁盘
# 查看UUID
sudo blkid
# 挂载到 /home/g/
mkdir /home/d/;
mkdir /home/g/;
# 写入文件
sudo echo '
# my D disk 
UUID=68D63746D6371432    /home/d    ntfs    defaults    0   0 
# my G disk 
UUID=96583C4C583C2D7D    /home/g    ntfs    defaults    0   0 ' >>  /etc/fstab ;
```


## <p id=8>修改启动等待时间

```bash
sudo vim /etc/default/grub

# 修改为=2
# GRUB_TIMEOUT = 10

sudo update-grub;
```

## <p id=9>github访问

```bash
echo 'cd lt 
# settings for github
192.30.253.112 github.com
151.101.44.249  github.global.ssl.fastly.net
' >> /etc/hosts;
```

## <p id=10>配置多JAVA共存

增加JAVA13，并配置多版本切换。[官网](http://jdk.java.net/13/)在此。准备好文件`openjdk-13.0.2_linux-x64_bin.tar.gz`到`/root/xiazai/`下。

```bash

tar -zvxf openjdk-13.0.2_linux-x64_bin.tar.gz -C /opt/;
sudo update-alternatives --install /usr/bin/java java /opt/jdk-13.0.2/bin/java 290
sudo update-alternatives --install /usr/bin/javac javac /opt/jdk-13.0.2/bin/javac 290
# 手动选择
sudo update-alternatives --config java
sudo update-alternatives --config javac
# 环境变量
echo '
# JAVA_13 SETTINGS
export JAVA13_HOME=/opt/jdk-13.0.2/
' >> ~/.bashrc;
source ~/.bashrc;
```
此处主要为elasticsearch 7.+准备。

## <p id=11>源码安装Cmake

[`cmake-3.15.2.tar.gz`](https://cmake.org/download/)

```bash
cd /root/xiazai;
tar -zxvf cmake-3.15.2.tar.gz -C /opt/;
cd /opt/cmake-3.15.2;
./bootstrap && make -j 8  && sudo make install
cmake --version
```

## <p id=12>shadowsocks in shell

在ubuntu 18.04 shell使用ss，需要安装ss + privoxy。

1. [shadowsocks-master.zip](https://github.com/shadowsocks/shadowsocks/archive/master.zip)

```bash
cd /root/xiazai;
unzip -d /opt/ master.zip

# build
cd /opt/shadowsocks-master
python3 setup.py build && python3 setup.py install
rm -f /usr/bin/sslocal
ln -s /usr/local/python/bin/sslocal /usr/bin/sslocal

# config
echo '
{
    "server": "hk5-sta41.f92i4.space",
    "server_port": 11673,
    "password": "a7kLhJgMdyruGsJ",
    "method": "chacha20-ietf-poly1305",
    "plugin": "",
    "plugin_opts": "",
    "remarks": "香港 5,数据用量倍率:1.00",
    "timeout": 300,
    "local_address": "127.0.0.1",
    "local_port":1081
} ' > /etc/shadowsocks/config.json

# run
nohup sslocal -c /etc/shadowsocks/config.json >> /logs/sslocal.log & 

# privoxy
apt install -y privoxy
echo '
forward-socks5t   /               127.0.0.1:10808 .
' >>  /etc/privoxy/config 
sudo /etc/init.d/privoxy restart

# try. default = 8118
wget -e "http_proxy=127.0.0.1:8118" www.google.com
curl -x 127.0.0.1:8118 www.google.com

# try in python3
import os,requests
os.environ['HTTP_PROXY']="http://127.0.0.1:8118"
os.environ['HTTPS_PROXY']="https://127.0.0.1:8118"
requests.get("http://google.com")
```

## <p id=13>拼音插件google云


```bash
sudo apt install -y fcitx
sudo apt install -y fcitx-googlepinyin

# 设置启动ficxy
im-config

# 附加组建部分点击添加google云
fcitx-config-gtk3

reboot
```

## <p id=14>搭建自有VPN

- 申请海外节点，并配置安全组规则。

```bash
sudo apt-get update;
sudo apt-get upgrade -y ;
sudo apt-get install -y make gcc curl python3-pip python3-setuptools net-tools openssh-server git unzip bc

mkdir /root/xiazai/;
cd /root/xiazai/;
wget https://github.com/shadowsocks/shadowsocks/archive/master.zip;
unzip -d /opt/ master.zip;

cd /opt/shadowsocks-master;
python3 setup.py build && python3 setup.py install;


echo '{
    "server":"::",
    "port_password": {
        "6666": "Xiong"
    },
    "timeout":300,
    "method":"rc4-md5",
    "fast_open": true
}' > /etc/shadowsocks.json;

#  open fast open
echo 3 > /proc/sys/net/ipv4/tcp_fastopen;
echo '
net.ipv4.tcp_fastopen = 3
' >> /etc/sysctl.conf 

ssserver -c /etc/shadowsocks.json -d restart
ssserver -c /etc/shadowsocks.json -d stop

# bbr协议
wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh && chmod +x bbr.sh && ./bbr.sh;
sysctl net.ipv4.tcp_available_congestion_control;

# 流量控制
wget https://github.com/hellofwy/ss-bash/archive/v1.0-beta.3.tar.gz;
tar -zxvf v1.0-beta.3.tar.gz;
mv ss-bash-1.0-beta.3 ss-bash;
cd ss-bash;

echo '"server": "0.0.0.0",
"timeout": 60,
"method": "rc4-md5",
"fast_open": true,' > ./ssmlt.template;

sudo ./ssadmin.sh add 55555 test 100m
sudo ./ssadmin.sh start
```

## <p id=15>内网穿透：frp服务



```bash
wget https://github.com/fatedier/frp/releases/download/v0.28.2/frp_0.28.2_linux_amd64.tar.gz
tar -zxvf frp_0.28.2_linux_amd64.tar.gz -C /opt/
mkdir  /logs/
nohup /opt/frp_*/frps -c /opt/frp_*/frps.ini >> /logs/frps.log &
nohup /opt/frp_*/frpc -c /opt/frp_*/frpc.ini >> /logs/frpc.log &
```



## <p id=16>jupyterlab


```bash
# install
pip install jupyterlab

# install node.js https://nodejs.org/zh-cn/
# export http_proxy=http://127.0.0.1:10809
# export https_proxy=http://127.0.0.1:10809
VERSION=v14.3.0
DISTRO=linux-x64
sudo mkdir -p /usr/local/lib/nodejs
wget https://nodejs.org/dist/$VERSION/node-$VERSION-$DISTRO.tar.xz --no-check-certificate
sudo tar -xJvf node-$VERSION-$DISTRO.tar.xz -C /usr/local/lib/nodejs 
# nodejs
echo "
export PATH=/usr/local/lib/nodejs/node-$VERSION-$DISTRO/bin:$PATH
" >> ~/.bashrc
source ~/.bashrc
node -v
npm version
# set to taobao
# npm config set registry https://registry.npm.taobao.org

# variableInspector
git clone https://github.com/lckr/jupyterlab-variableInspector
cd jupyterlab-variableInspector
npm install
npm run build
jupyter labextension install .
# latex
pip install jupyterlab_latex
jupyter labextension install @jupyterlab/latex
# drawio
jupyter labextension install jupyterlab-drawio
# check
jupyter labextension list
# uninstall
jupyter labextension uninstall my-extension
# run in win10
start /b jupyter lab --notebook-dir 'D:\github_work' >nul 2>nul
# run in ubuntu
jupyter lab xxx
```



# <p id=17>shell代理

```bash
echo '
# V2RAY FOR SHELL
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:10808"
alias unsetproxy="unset ALL_PROXY"
' >> ~/.bashrc
source ~/.bashrc
```

# torch7 under cuda10

GNN用到facebook的bAbi数据集，需要安装torch和luarocks

#### torch 7.0

from:  https://github.com/nagadomi/waifu2x/issues/253 

```bash
git clone https://github.com/nagadomi/distro.git ~/torch --recursive
cd ~/torch
./install-deps
./clean.sh
./update.sh
. ~/torch/install/bin/torch-activate
```

#### luarocks

 https://github.com/luarocks/luarocks/wiki/installation-instructions-for-unix 

```bash
# lua
sudo apt install build-essential libreadline-dev
curl -R -O http://www.lua.org/ftp/lua-5.3.4.tar.gz
tar -zxf lua-5.3.4.tar.gz
cd lua-5.3.4
make linux test
sudo make install
# luarocks
wget https://luarocks.org/releases/luarocks-3.2.1.tar.gz
tar zxpf luarocks-3.2.1.tar.gz
cd luarocks-3.2.1
./configure
make build
make install
```

#### bAbi

```bash
./babi-tasks 1 1000 > task_1.txt
./babi-tasks 1 500 --symbolic true > symbolic_task_1.txt
echo ' data looks like: 
1 D {} N
2 E {} J
3 eval D is_in  N       1
'
```



# 查看网速

```bash
git clone https://github.com/rolandriegel/nload.git
cd nload
./run_autotools
./configure && make -j 4 
sudo make install
nload enp3s0 -u M
echo "
alias show_net_speed='nload enp3s0 -u M'
" >> ~/.bashrc
source ~/.bashrc
```

# 文件转换fromdos

windows和unix文件转换。

```bash
# 方法1
sudo apt-get install tofrodos 
echo "
alias unix2dos=todos alias dos2unix=fromdos
" >> ~/.bashrc
# 方法2
tr -d "\15\32" < ./123.txt > 123.txt
```

## 设置apt代理

```bash
echo 'Acquire::socks5::proxy "socks://127.0.0.1:1080/";' >> /etc/apt/apt.conf.d/proxy.conf
```

## teamviewer

```bash
sudo dpkg -i teamviewer_amd64.deb
sudo apt install -y -f
sudo apt install ./teamviewer_amd64.deb
sudo apt autoremove -y
teamviewer passwd xiongxiong
teamviewer --daemon restart
teamviewer info
```



## APEX and CUDA

```bash
# cuda 10.1
wget https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.105_418.39_linux.run
sudo sh cuda_10.1.105_418.39_linux.run
echo '
# settings for cuda 
export CUDA_HOME=/usr/local/cuda-10.1
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATH
export PATH=$PATH:CUDA_HOME:$LD_LIBRARY_PATH
' >> ~/.bashrc
source ~/.bashrc

# 临时升级gcc
yum -y install centos-release-scl devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils
scl enable devtoolset-7 bash

# apex
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```

# 多进程压缩

```bash
# 分卷
tar --use-compress-program=pigz -cpf - test | split -b 4095m -d - test.tar.gz
# 打包
tar --use-compress-program=pigz -cvpf test.tgz ./test
# 解包
tar --use-compress-program=pigz -xvpf test.tgz -C ./test

tar -czf - proc | split -b 2m -d - proc.tar.gz
```

## 别名合集

wget打印到标准输出：`wget -e 'https_proxy=http://127.0.0.1:10809' https://www.google.com -O -`

```bash
echo -e '
# my alias.
alias lll="ll -hla"
alias curl_google="curl -x socks5://127.0.0.1:10808 https://www.google.com"
alias wget_google="wget -e \047https_proxy=http://127.0.0.1:10809\047 https://www.google.com"
alias setproxy="export http_proxy=http://127.0.0.1:10809; export https_proxy=http://127.0.0.1:10809"
alias unsetproxy="unset http_proxy; unset https_proxy;"
' >> ~/.bashrc
source ~/.bashrc

```


