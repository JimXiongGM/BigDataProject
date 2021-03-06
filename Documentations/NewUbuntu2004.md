## <p id=1>更新apt源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list_backup;
sudo echo '#阿里源
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
' > /etc/apt/sources.list;

sudo apt-get update;
sudo apt-get -y upgrade;
# change pip source
mkdir ~/.pip;
echo '[global]
timeout = 6000
index-url = http://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com' > ~/.pip/pip.conf;
```

或者保持[20.04原始源](XXXXXXXX), 使用代理.

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

## <p id=3>root账户

### 密码与ssh

`sudo passwd`
`ssh-keygen`

开启root远程登录权限.
```bash
echo '
# settings for root login in 
PermitRootLogin yes
' >> /etc/ssh/sshd_config
# 重启ssh
/etc/init.d/ssh restart
```


## anaconda

**先安装anaconda, 再安装CUDA环境.**

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh
```

使用更加灵活的方式启动jupyter.
```shell
# ipython
In [1]: from notebook.auth import passwd
In [2]: passwd()
In [3]: exit

echo "
c.NotebookApp.password = u'sha1:10e617836771:f85d187eb26c0e7ce761fee8ea42044da3df2a8b'
" > ~/.jupyter_config_passwd.py;

# 当前目录启动
nohup jupyter lab --config ~/.jupyter_config_passwd.py --ip 0.0.0.0 --port 5946 --notebook-dir ./ --no-browser --allow-root >> ./jupyterlab.log &
```

插件
```
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user --skip-running-check
jupyter nbextensions_configurator enable --user
```

切换源

```bash
echo 'channels:
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
show_channel_urls: true' > ~/.condarc

# 恢复
echo 'channels:
  - defaults
show_channel_urls: true' > ~/.condarc
```

新增环境
```bash
conda create -n coarse2fine python=3.5
conda activate coarse2fine
conda install -y ipykernel
python -m ipykernel install --user --name coarse2fine --display-name "coarse2fine"
```

删除环境
```
conda remove -n coarse2fine --all
```


## root用户彩色显示

在`~/.bashrc`下添加:
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
`source ~/.bashrc`即可.


## 安装cuda10.1/10.2+cudnn

实测apex在cuda10.1+ubuntu 20.04+gcc 8.4.0 下不能通过编译. 10.2可以. 这里选择安装两个版本的cuda, 有需要时切换(见`alias`).

```bash
# 增加gcc 8. 实测6也可以
sudo apt -y install build-essential
sudo apt -y install gcc-8 g++-8 gcc-9 g++-9

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8 --slave /usr/bin/g++ g++ /usr/bin/g++-8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9 --slave /usr/bin/g++ g++ /usr/bin/g++-9

# 选择gcc 9.
sudo update-alternatives --config gcc

sudo bash NVIDIA-Linux-x86_64-440.82.run
# 提示如下: One or more modprobe....
sudo update-initramfs -u
sudo reboot
sudo bash NVIDIA-Linux-x86_64-440.82.run
nvidia-smi

# CUDA Toolkit and cuDNN
# Switch gcc to gcc-8
sudo update-alternatives --config gcc

# Run installer, accept license, deselect Driver
wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run
sudo bash cuda_10.2.89_440.33.01_linux.run

echo '
# CUDA settings
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CUDA_HOME/extras/CUPTI/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc;
source ~/.bashrc;

wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/cudnn-10.2-linux-x64-v7.6.5.32.tgz
sudo tar -zxvf cudnn-10.2-linux-x64-v7.6.5.32.tgz

cp ./cuda/include/cudnn.h ${CUDA_HOME}/include/
cp ./cuda/lib64/libcudnn* ${CUDA_HOME}/lib64/
# 注意root可能没有CUDA_HOME
sudo chmod a+r ${CUDA_HOME}/include/cudnn.h
sudo chmod a+r ${CUDA_HOME}/lib64/libcudnn*

sudo rm ${CUDA_HOME}/targets/x86_64-linux/lib/libcudnn.so.7 ${CUDA_HOME}/targets/x86_64-linux/lib/libcudnn.so
sudo ln -s libcudnn.so.7.6.5 ${CUDA_HOME}/targets/x86_64-linux/lib/libcudnn.so.7
sudo ln -s libcudnn.so.7 ${CUDA_HOME}/targets/x86_64-linux/lib/libcudnn.so
sudo ldconfig
```

output:
```
One or more modprobe configuration files to disable Nouveau have been written.  For some distributions, this may be sufficient to disable Nouveau; other distributions may require modification of the initial ramdisk.  Please reboot your system and attempt NVIDIA driver 
  installation again.  Note if you later wish to reenable Nouveau, you will need to delete these files: /usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf, /etc/modprobe.d/nvidia-installer-disable-nouveau.conf
```

切换cuda版本
```bash
rm -rf /usr/local/cuda #删除之前创建的软链接
sudo ln -s /usr/local/cuda-9.2/ /usr/local/cuda
nvcc --version #查看当前 cuda 版本
```

## Pytorch and TensorFlow and apex

```bash
pip install --upgrade pip

# pt
pip install torch torchvision
python -c "import torch; print(torch.cuda.is_available())"

# tf2 不支持 cuda 10.2
# pip install tensorflow
# python -c "import tensorflow as tf; tf.config.list_physical_devices('GPU')"
# python -c "import tensorflow as tf; print(tf.constant(2.0)*tf.constant(4.0))"


# apex gcc 8 passed.
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 10
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 20
sudo update-alternatives --config g++
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
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

exit 0' > /etc/rc.local;

sudo chmod +x /etc/rc.local;
sudo systemctl enable rc-local;

sudo systemctl start rc-local.service;
sudo systemctl status rc-local.service;
```


## <p id=7>永久挂载硬盘

```bash
## 旧磁盘
# 查看UUID
sudo lsblk
sudo blkid
# 挂载到 /home/g/
mkdir /home/d/;
mkdir /home/g/;
# 写入文件
sudo echo '
# my h disk 
UUID=60072F263C035B63    /home/h    ntfs    defaults    0   0 
# my g disk 
UUID=0A0896E20896CBD7    /home/g    ntfs    defaults    0   0 ' >>  /etc/fstab ;
```

## teamviewer

```bash
wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb
sudo dpkg -i teamviewer_amd64.deb
sudo apt install -y -f
sudo apt install ./teamviewer_amd64.deb
sudo apt autoremove -y
teamviewer passwd xiongxiong
teamviewer --daemon restart
teamviewer info
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
alias nvidia_watch="watch -n 1 nvidia-smi"
alias git_sync="git fetch --all && git reset --hard origin/master && git pull"
alias switch_cuda101="sudo rm -rf /usr/local/cuda && sudo ln -s /usr/local/cuda-10.1/ /usr/local/cuda && nvcc --version"
alias switch_cuda102="sudo rm -rf /usr/local/cuda && sudo ln -s /usr/local/cuda-10.2/ /usr/local/cuda && nvcc --version"
alias switch_cuda90="sudo rm -rf /usr/local/cuda && sudo ln -s /usr/local/cuda-9.0/ /usr/local/cuda && nvcc --version"
' >> ~/.bashrc
source ~/.bashrc
```

## github加速

```bash
git config --global user.name "JimXiongGM"
git config --global user.email gm_xiong@qq.com
sudo echo '
# GitHub hosts 
192.30.253.112    github.com 
192.30.253.119    gist.github.com
151.101.184.133    assets-cdn.github.com
151.101.184.133    raw.githubusercontent.com
151.101.184.133    gist.githubusercontent.com
151.101.184.133    cloud.githubusercontent.com
151.101.184.133    camo.githubusercontent.com
151.101.184.133    avatars0.githubusercontent.com
151.101.184.133    avatars1.githubusercontent.com
151.101.184.133    avatars2.githubusercontent.com
151.101.184.133    avatars3.githubusercontent.com
151.101.184.133    avatars4.githubusercontent.com
151.101.184.133    avatars5.githubusercontent.com
151.101.184.133    avatars6.githubusercontent.com
151.101.184.133    avatars7.githubusercontent.com
151.101.184.133    avatars8.githubusercontent.com
151.101.185.194    github.global.ssl.fastly.ne
' >> /etc/hosts
```

## 输入法

```bash
curl -sL 'https://keyserver.ubuntu.com/pks/lookup?&op=get&search=0x73BC8FBCF5DE40C6ADFCFFFA9C949F2093F565FF' | sudo apt-key add
sudo apt-add-repository 'deb http://archive.ubuntukylin.com/ukui focal main'
sudo apt upgrade
sudo apt install -y sogouimebs
sogouIme-configtool 

# 如果无法卸载ibus可以采用禁用ibus的方法。
sudo dpkg-divert --package im-config --rename /usr/bin/ibus-daemon

# 启用ibus方法。
sudo dpkg-divert --package im-config --rename --remove /usr/bin/ibus-daemon
```

进入设置，选择“区域与语言”，点击管理已安装的语言，把默认输入法设置为fcitx，重启电脑就可以使用搜狗输入法了。


## ERRORs

TensorFlow 2.1+设置显存的trick：

```bash
import tensorflow as tf
gpus= tf.config.list_physical_devices('GPU') # tf2.1版本该函数不再是experimental
print(gpus) # 前面限定了只使用GPU1(索引是从0开始的,本机有2张RTX2080显卡)
tf.config.experimental.set_memory_growth(gpus[0], True) # 其实gpus本身就只有一个元素
```


## JAVA

```bash
# 下载 jdk-8u261-linux-x64.tar.gz from https://www.oracle.com/cn/java/technologies/javase/javase-jdk8-downloads.html
tar -zxvf jdk-8u261-linux-x64.tar.gz -C /home/jimx/opt/

echo '
# JAVA SETTINGS
export JAVA_HOME=/home/jimx/opt/jdk1.8.0_261
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

java -version
```


## 升级卸载内核


```bash
# 升级
# https://kernel.ubuntu.com/~kernel-ppa/mainline/  下载deb文件
sudo dpkg -i *.deb

# 卸载
dpkg --get-selections | grep linux
sudo apt-get purge -y \
  linux-headers-5.4.0-42 \
  linux-headers-5.4.0-42-generic \
  linux-image-5.4.0-42-generic \
  linux-modules-5.4.0-42-generic \
  linux-modules-extra-5.4.0-42-generic

sudo update-grub2  #根据情况选择grub/grub2
```
