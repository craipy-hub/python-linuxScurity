# python-LinuxSecurity
## 描述：
利用python实现对linux系统文件进行保护。

首先通过Init.py建立初始化数据库，保存系统中文件的inode信息和md5信息

后面利用Check.py检查系统中文件的属性是否更改，文件md5是否变动等信息判断系统文件被改动的部分

分为3类文件
1. 新增文件
2. 被修改文件
3. 被删除文件

## 环境

python3+Sqlite+zmail

## 项目文件说明

├── Check.py <br>
├── data <br>
│   ├── init.db <br>
│   └── test.db <br>
├── etc <br>
│   └── pol.txt <br>
├── Init.py <br>
├── lib <br>
│   ├── Config.py <br>
│   ├── DBOperateOld.py <br>
│   ├── DBOperate.py <br>
│   ├── Email.py <br>
│   ├── FileOperate.py <br>
│   ├── FormatInfo.py <br>
│   ├── \__init__.py <br>
│   ├── MD5.py <br>
│   ├── MyStat.py <br>
│   └── Policy.py <br>
├── PrintReport.py <br>
├── README.md <br>
└── tset.py <br>

## data
文件夹下存放数据库文件，数据库使用的sqlite

## etc
文件夹下存放的是配置文件 pol.txt针对文件某些属性被修改进行捕捉

## lib
文件夹下是项目运行需要用到函数库。

### Config.py
文件包含了项目路径，配置文件路径，数据库文件路径等等

后期添加一些辅助功能的相关配置会在这里进行

比如：

1. 定时执行Check，定时的规则
2. 是否配置邮箱，当发现有异常文件改动时，主动发送邮箱
3. 后面如果有其他功能再添加

### DBOperate.py
文件是进行数据库操作时所用到的一些语句的生成函数，创建表，插入数据，更新数据等等

### DBOperateOld.py
已经弃用，原本打算用ORM框架进行数据库操作，但是在非常多的文件面前，peewee运行效率极其低下，20分钟才存2万条数据

### Email.py
是用来配置发送邮件的

### FileOperate.py
里面包含了文件属性，文件路径收集的函数

### FormatInfo.py
是用来格式化文件属性用的，由于stat获取到的文件属性都是int型数据，需要通过一些函数格式化为便于人们理解的字符串。

### MD5.py
里面包含了读取计算文件md5值得函数

### MyStat.py
中包含了Mystat类，用于将stat信息转换为类或者字典，便于调用操作


## 最外层的三个文件

### PrintReport.py
文件是用来在Check之后生成报告，并输出给用户看的

### Init.py
文件是用来建立初始化数据库的

### Check.py
是用来检查文件改动的
