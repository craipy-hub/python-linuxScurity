# python-LinuxSecurity
## 描述：
利用python实现对linux系统文件进行保护。
首先通过Init.py建立初始化数据库，保存系统中文件的inode信息和md5信息
后面利用Check.py检查系统中文件的属性是否更改，文件md5是否变动等信息判断系统文件被改动的部分
分为3类文件
1. 新增文件
2. 被修改文件
3. 被删除文件
