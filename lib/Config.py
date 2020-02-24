import os

# 项目目录
ProjectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据存放目录
dataDir = os.path.join(ProjectDir,'data')

# 初始数据库路径
initDB_Path = os.path.join(dataDir,'init.db')

# 配置文件存放目录
etcDir = os.path.join(ProjectDir,'etc')

# 配置文件路径
policyPath = os.path.join(etcDir,'pol1.txt')

