# 知识图谱数据库


## virtuoso

https://github.com/openlink/virtuoso-opensource

系统：ubuntu 20.04.1

```bash
# 一次点亮
sudo apt install -y autoconf automake flex bison gperf gawk m4 libssl-dev

autoconf --version
automake --version
libtoolize --version  # 系统自带：libtoolize (GNU libtool) 2.4.6
flex --version
bison --version
gperf --version
gawk --version
m4 --version
make --version   # 系统自带：GNU Make 4.2.1
openssl version   # 系统自带：OpenSSL 1.1.1g  21 Apr 2020

./autogen.sh        # should only be needed in git clone
CFLAGS="-O2 -m64"
export CFLAGS
./configure
make -j8
make install

echo '
# virtuoso settings
export PATH=/usr/local/virtuoso-opensource/bin:$PATH
' >> ~/.bashrc && source ~/.bashrc

# Test Suite
make check

# Getting Started
sudo chown -R jimx /usr/local/virtuoso-opensource
cd /usr/local/virtuoso-opensource/var/lib/virtuoso/db/
virtuoso-t -f &
```

http://localhost:8890/sparql/
