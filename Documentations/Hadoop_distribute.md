# Hadoop3的全分布式安装 
这一部分的环境在笔者开始记录之前已经搭建好，站在巨人的肩膀上[@daviddwlee84](https://github.com/daviddwlee84)，我才能较快地搭建好全分布式Hadoop。这位同学的主要贡献是利用Python中的fabric包，实现了一键自动安装Hadoop3.1.1，不过他的环境是4块树莓派3b+，并基于本地局域网。[链接](https://github.com/daviddwlee84/RaspPi-Cluster)在此。  

他山之石，虽可攻玉，但是环境不同，总是有各种各样的bug。这里记录一下。

- 1.首先，动员你的小伙伴申请阿里云服务器，我这一共申请了5台。
- 2.将5台服务器的公网ip和内网ip都记下来，并且登陆每一台机器，使用`sudo vim /etc/hosts`修改host文件，注释localhost，并且按照如下格式添加：  
> 内网ip master.local  
> 对应公网ip slave1.local  
> 对应公网ip slave2.local  
> 对应公网ip slave3.local  
> 对应公网ip slave4.local  
- 特别要**注意**的是，配置XX结点的时候，对应自己的ip要填写为内网ip，否则会出现奇怪的bug..
- 3.接着登陆每一台机器配置`sudo vim /etc/hostname`，分别是master.local，slave[1-5].local。至于为什么要这么配置呢？因为大佬同学写好的一键安装程序是这么命令的...在配置Hadoop的时候，需要将hostname写入配置文件，因此如果需要更名比较麻烦，笔者偷懒，直接使用已有的环境。>.<
- 4.**非常重要**的一点，阿里云默认只开放22，8080等几个端口，这显然是不行的。我们需要登陆所有机器的阿里云控制台，手动修改端口访问权限。我这里非常不安全地开放了所有的端口。
- 5.仔细研读daviddwlee84的[Usage in Detail](https://github.com/daviddwlee84/RaspPi-Cluster/blob/master/Documentation/FabfileHelp.md)，一键安装、一键调试等功能能极大地方便我们搭建环境，从而focus on the data analysis work .
- that is all，以后有机会再重新搭建一次，再更新。