# Stanford CoreNLP

https://stanfordnlp.github.io/CoreNLP/download.html#getting-a-copy

当前：CoreNLP 4.2.0


upudate

```
VERSION=stanford-corenlp-4.2.0
cd xiazai_sys
wget http://nlp.stanford.edu/software/stanford-corenlp-latest.zip
wget http://nlp.stanford.edu/software/$VERSION-models-chinese.jar

unzip stanford-corenlp-latest.zip
mv $VERSION-models-chinese.jar $VERSION/

cd /home/jimx/xiazai_sys/$VERSION
export CLASSPATH=$CLASSPATH:/home/jimx/xiazai_sys/$VERSION/*:

# Run the server using all jars in the current directory (e.g., the CoreNLP home directory)
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# Run a server using Chinese properties
java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties -port 9001 -timeout 15000

# test
wget --post-data '斯坦福自然语言处理工具' 'localhost:9100/?properties={"annotators": "tokenize,ssplit,pos", "outputFormat": "json"}' -O -
```


## sutime

```bash
pip install setuptools_scm jpype1 # install pre-reqs
pip install sutime
# use package pom.xml to install all Java dependencies via Maven into ./jars
git@github.com:FraBle/python-sutime.git
cd python-sutime
mvn dependency:copy-dependencies -DoutputDirectory=./jars

# 修改 /home/jimx/anaconda3/envs/sparqa/lib/python3.8/site-packages/sutime/sutime.py
# 根据 ./jars 下的版本，修改为：
    _required_jars = {
        'stanford-corenlp-3.9.2-models.jar',
        'stanford-corenlp-3.9.2.jar',
        'gson-2.8.5.jar',
        'slf4j-simple-1.7.25.jar'
    }

# 最后一行改为：
        if reference_date:
            return json.loads(str(self._sutime.annotate(input_str, reference_date)))
        return json.loads(str(self._sutime.annotate(input_str)))
```

```python
# 测试：
# 首先添加corenlp的环境变量
import json
import os
from sutime import SUTime

if __name__ == '__main__':
    test_case = u'I need a desk for tomorrow from 2pm to 3pm'

    jar_files = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars="/home/jimx/codes/SPARQA/python-sutime/jars", mark_time_ranges=True)

    # sutime = SUTime(jars='/home/jimx/codes/SPARQA/resources_sutime/python-sutime-master/jars', mark_time_ranges=True)

    res1 = sutime.parse(test_case)
    res2 = json.dumps(res1)

    print(json.dumps(sutime.parse(test_case), sort_keys=True, indent=4))
```


import tensorflow as tf
 

with tf.device('/gpu:0'):
    c = a+b
   
#注意：allow_soft_placement=True表明：计算设备可自行选择，如果没有这个参数，会报错。
#因为不是所有的操作都可以被放在GPU上，如果强行将无法放在GPU上的操作指定到GPU上，将会报错。
sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,log_device_placement=True))
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
sess.run(tf.global_variables_initializer())
print(sess.run(c))

