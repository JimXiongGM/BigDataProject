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
sudo apt-get upgrade;
sudo apt-get update;
# change pip source
mkdir ~/.pip;
echo '[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com' > ~/.pip/pip.conf;

```

## <p id=2>常用依赖安装

```bash
sudo apt-get install -y make;
sudo apt-get install -y gcc;
sudo apt-get install -y curl;
sudo apt-get install -y python3-pip;
sudo pip3 install -i http://pypi.douban.com/simple/ --trusted-host --upgrade pip;
sudo apt-get install -y net-tools;
sudo apt-get install -y openssh-server;
sudo apt-get install -y git;
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

在`/etc/bash.bashrc`下添加如下内容即可。内容来源于`~/.bashrc`文件
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
`source /etc/bash.bashrc`即可。

## <p id=4>源码安装Python3.7

```bash
# 先安装openssl
cd /root/xiazai;
wget http://www.openssl.org/source/openssl-1.1.1.tar.gz;
tar -zxvf openssl-1.1.1.tar.gz;
cd openssl-1.1.1;
./config --prefix=/usr/local/openssl shared zlib;
make -j 8 && make install;

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib" >> /etc/bash.bashrc
source /etc/bash.bashrc

# 接着安装sqlite3
wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz;
tar -xzvf  sqlite-autoconf-3290000.tar.gz;
cd sqlite-autoconf-3290000;
./configure --disable-tcl --prefix="/usr/local/sqlite3";
make -j 8 && make install;

# 编译安装Python3
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz;
tar -xvf Python-3.7.2.tar.xz;
cd Python-3.7.2;

echo '
# settings for openssl
_socket socketmodule.c
SSL=/usr/local/openssl
_ssl _ssl.c \
       -DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
       -L$(SSL)/lib -lssl -lcrypto' >> ./Modules/Setup.dist;

./configure --prefix=/usr/local/python --with-ssl LDFLAGS="-L/usr/local/sqlite3/lib" CPPFLAGS="-I/usr/local/sqlite3/include" ;
make -j 8 && make install

# 解决 apt_pkg问题
sudo apt-get remove --purge python-apt;
sudo apt-get install python-apt -f;
# sudo find / -name "apt_pkg.cpython-35m-x86_64-linux-gnu.so"
cd /usr/lib/python3/dist-packages/;
sudo cp apt_pkg.cpython-36m-x86_64-linux-gnu.so apt_pkg.cpython-37m-x86_64-linux-gnu.so
```

## <p id=5>安装cuda

### for pytorch

1. 安装ubuntu的时候就要设置，在`quiet splash`这一行的末尾加上` acpi_osi=linux nomodeset`。
2. 在软件管理器的附加驱动中可视化安装NVIDIA驱动。（命令行模式安装失败）

[CUDA官网]
(https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal)。运行如下代码即可。

```bash
cd xiazai;
wget https://developer.download.nvidia.cn/compute/cuda/10.1/secure/Prod/local_installers/cuda_10.1.168_418.67_linux.run?3vrspqMCpTwuoe3kCBSQ6dHRXI4lW_MTKJrLwnti8jK8qobgEieoN7dT-trbRszIC8G2WOQv2mbuQic8myzK9EoC6bz_v0hHI8ABajYaBAEs96mfrZ7oZnlKk5mYlrola2gEQXJKvxWdqlqU1EUdzTtyGyO7YVdxBjC8RnqDLXrY-K6XuGNYDVlzy18;

echo '
# CUDA settings
export CUDA_HOME=/usr/local/cuda-10.1
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64 
export PATH=${CUDA_HOME}/bin:${PATH}
' >> /etc/bash.bashrc;
source /etc/bash.bashrc;

# 验证结果
nvidia-smi
# 会弹出可视化窗口
nvidia-settings
# 实时查看GPU情况
watch -n 1 nvidia-smi
```

### for tensorflow 2.0

[TF-GPU官网](https://www.tensorflow.org/install/gpu)

上文已完成前两个。

- [x] NVIDIA® GPU 驱动程序 - CUDA 10.0 需要 410.x 或更高版本。
- [x] CUDA® 工具包 - TensorFlow 支持 CUDA 10.0（TensorFlow 1.13.0 及更高版本）
- [ ] CUDA 工具包附带的 CUPTI。
- [ ] cuDNN SDK（7.4.1 及更高版本）
- [ ] （可选）[TensorRT 5.0](https://developer.nvidia.com/nvidia-tensorrt-5x-download#trt51ga)，可缩短在某些模型上进行推断的延迟并提高吞吐量。

还需要

1. [cudnn-10.1-linux-x64-v7.6.2.24.tgz](https://developer.nvidia.com/cudnn)
2. [nv-tensorrt-repo-ubuntu1804-cuda10.1-trt5.1.5.0-ga-20190427_1-1_amd64.deb](https://developer.nvidia.com/tensorrt)

```bash
# CUPTI
echo '
# SETTINGS FOR TF2.0-GPU
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/extras/CUPTI/lib64
' >> /etc/bash.bashrc ;
source /etc/bash.bashrc;

# cudnn-10.1
tar -zxvf cudnn-10.1-linux-x64-v7.6.2.24.tgz -C /opt/;
sudo cp /opt/cuda/include/cudnn.h /usr/local/cuda/include/
sudo cp /opt/cuda/lib64/libcudnn* /usr/local/cuda/lib64/
sudo chmod a+r /usr/local/cuda/include/cudnn.h
sudo chmod a+r /usr/local/cuda/lib64/libcudnn*

# 解决CUDA10.1不兼容问题
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcudart.so.10.1 /usr/local/cuda-10.1/lib64/libcudart.so.10.0
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcublas.so.10.1 /usr/local/cuda-10.1/lib64/libcublas.so.10.0
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcufft.so.10.1 /usr/local/cuda-10.1/lib64/libcufft.so.10.0
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcurand.so.10.1 /usr/local/cuda-10.1/lib64/libcurand.so.10.0
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcusolver.so.10.1 /usr/local/cuda-10.1/lib64/libcusolver.so.10.0
ln -s /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcusparse.so.10 /usr/local/cuda-10.1/lib64/libcusparse.so.10.0


sudo dpkg -i libcudnn7_7.6.2.24-1+cuda10.1_amd64.deb
sudo dpkg -i nv-tensorrt-repo-ubuntu1804-cuda10.1-trt5.1.5.0-ga-20190427_1-1_amd64.deb

# 进入python3
python3

import tensorflow as tf
print("GPU Available: ", tf.test.is_gpu_available())
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
# 查看UUID
df -h;
# 挂载到 /home/d/
mkdir /home/d/;
# 写入文件
sudo echo '
# my D disk 
UUID=563C05B33C058EE5    /home/d    ntfs    defaults    0   0 ' >>  /etc/fstab ;
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

增加JAVA12，并配置多版本切换。准备好文件`jdk-12.0.2_linux-x64_bin.tar.gz`到`/root/xiazai/`下。

```bash
cd xiazai;
tar -zvxf jdk-12.0.2_linux-x64_bin.tar.gz -C /opt/;
sudo update-alternatives --install /usr/bin/java java /opt/jdk-12.0.2/bin/java 290
sudo update-alternatives --install /usr/bin/javac javac /opt/jdk-12.0.2/bin/javac 290
# 手动选择
sudo update-alternatives --config java
sudo update-alternatives --config javac
# 环境变量
echo '
# JAVA_12 SETTINGS
export JAVA12_HOME=/opt/jdk-12.0.2/
' >> /etc/bash.bashrc;
source /etc/bash.bashrc;
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
