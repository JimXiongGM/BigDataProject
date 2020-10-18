# NewMacOS

系统：catalina 

```bash
# 激活井号注释模式
setopt interactivecomments

# github访问443
echo '
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
151.101.185.194    github.global.ssl.fastly.net 
' >> /etc/hosts

# GitHub配置 http下的用户名密码
git config --global user.name "JimXiongGM"
git config --global user.email gm_xiong@qq.com
git config --global credential.helper store

# 安装homebrew，终端挂代理
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" 

brew install watch
brew install wget

echo '
# history设置
export HISTTIMEFORMAT="%Y-%M-%D %H:%M:%S  " 
PROMPT_COMMAND="history -a"
'
>> ~/.zshrc
source ~/.zshrc

# 移动硬盘只读问题
hdiutil eject /Volumes/WD\ Security # 弹出移动硬盘
hdiutil eject /Volumes/WD\ Unlocker
hdiutil eject /Volumes/My\ Passport\ XGM
sudo mkdir /Volumes/MYHD  # 建立新的目录
diskutil info /Volumes/My\ Passport\ XGM  # 查看Device Node：/dev/disk2s0s2
sudo mount_ntfs -o rw,nobrowse /dev/disk4s1 /Volumes/MYHD/  # 挂载到自定义的文件夹
sudo umount /Volumes/MYHD/ # 卸载

# host
sudo echo '
# settings
192.168.0.103 house
' >> /etc/hosts
```

