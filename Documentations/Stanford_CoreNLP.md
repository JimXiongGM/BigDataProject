# Stanford CoreNLP

https://stanfordnlp.github.io/CoreNLP/download.html#getting-a-copy

当前：CoreNLP 4.1.0


```bash
java -version

wget http://nlp.stanford.edu/software/stanford-corenlp-latest.zip

unzip stanford-corenlp-latest.zip

cd stanford-corenlp-4.0.0

for file in `find /home/jimx/xiazai_sys/stanford-corenlp-4.1.0/ -name "*.jar"`; do export
CLASSPATH="$CLASSPATH:`realpath $file`"; done

echo "the quick brown fox jumped over the lazy dog" > input.txt
java -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -outputFormat json -file input.txt

# 快速启动
echo '
# corenlp
for file in `find . -name "*.jar"`; do export
CLASSPATH="$CLASSPATH:`realpath $file`"; done
' > ~/stanford_CoreNLP_addPATH.sh

echo '
alias stanford_CoreNLP_addPATH="bash ~/stanford_CoreNLP_addPATH.sh"
' >> ~/.bashrc
source ~/.bashrc

# server
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
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