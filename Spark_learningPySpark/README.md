# PySpark初探

本上手项目内容均来自Tomasz Drabas 和 Denny Lee的著作《Learning PySpark》，译作为《PySpark实战指南》。本书提供了大量代码供读者运行，这里笔者放上自己的阅读笔记和运行结果。

原著直接在[databricks](https://community.cloud.databricks.com/login.html)平台运行Python代码，这个平台免费提供6GB内存的spark实例供学习使用，且集成scala，能够非常方便地实现数据可视化。缺点是免费spark实例只有2小时活跃时间，且笔者个人认为databricks没有jupyter notebook好用。因此笔者选择自行搭建平台run代码，除了第7章。

第7章介绍GraphFrames包。由于databricks平台能够在cell中直接运行scala，但jupyter不行，因此原书代码中大量可视化效果无法显示。于是笔者选择在databricks进行实验并保存为html。

原著github地址：https://github.com/drabastomek/learningPySpark。本目录下提供了上述github的zip包。

具体内容均在相应的jupyter notebook中，如下所示。

||第4章：准备数据建模|第5章：MLlib介绍|第6章：ML包介绍|第7章：GraphFrames介绍
---|---|---|---|---
html版本|[√](./LearningPySpark_Chapter04_笔记版.html)|[√](./LearningPySpark_Chapter05_笔记版.html)|[√](./LearningPySpark_Chapter06_笔记版.html)|[√](./LearningPySpark_Chapter07_笔记版.html)
ipynb版本|[√](./LearningPySpark_Chapter04_笔记版.ipynb)|[√](./LearningPySpark_Chapter05_笔记版.ipynb)|[√](./LearningPySpark_Chapter06_笔记版.ipynb)|[√](./LearningPySpark_Chapter07_笔记版.ipynb)

