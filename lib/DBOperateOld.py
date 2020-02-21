import lib.Config
from peewee import *
db = SqliteDatabase(lib.Config.initDB_Path)
# db.connect()
class BaseModel(Model):
    u"""
    基础类
    可以在此处制定一些大家都需要的列，
    然后每个继承的子类（表）中都会有这么固定的几列
    """

    class Meta:
        u"""指定数据库."""
        database = db

class FILEDB(BaseModel):
    PATH = CharField(verbose_name='文件路径',max_length=600,primary_key=True,index=True,null=False)
    STAT = CharField(verbose_name='文件属性', null=True,default='1')
    MD5 = CharField(verbose_name='文件的MD5值',max_length=64, null=True,default='1')
    Rule_Type = CharField(verbose_name='文件的规则名称',max_length=30, null=True,default='1')
    Rule_Check = CharField(verbose_name='文件检查项',max_length=20, null=True, default='1')
    Record = CharField(verbose_name='文件状态记录',max_length=1, null=True,default='o')

def create_table(table):
    u"""
    如果table不存在，新建table
    """
    if not table.table_exists():
        table.create_table()

def drop_table(table):
    u"""
    table 存在，就删除
    """
    if table.table_exists():
        table.drop_table()
