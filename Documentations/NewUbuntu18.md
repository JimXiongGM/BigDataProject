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

## <p id=2>基本依赖安装

```bash
sudo apt-get install -y make;
sudo apt-get install -y gcc;
sudo apt-get install -y curl;
sudo apt-get install -y python3-pip;
sudo pip3 install -i http://pypi.douban.com/simple/ --trusted-host --upgrade pip;
sudo apt-get install -y net-tools;
sudo apt-get install -y openssh-server;
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
make -j 4 && make install;

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib" >> /etc/bash.bashrc
source /etc/bash.bashrc

# 接着安装sqlite3
wget https://www.sqlite.org/2019/sqlite-autoconf-3290000.tar.gz;
tar -xzvf  sqlite-autoconf-3290000.tar.gz;
cd sqlite-autoconf-3290000;
./configure --disable-tcl --prefix="/usr/local/sqlite3";
make -j 8 && make install;

# 安装Python3
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
ls
```

## <p id=5>安装cuda

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