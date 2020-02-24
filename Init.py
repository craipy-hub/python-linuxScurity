from lib.FileOperate import getDirData,collectFileData
from lib.Policy import setRule
from lib.Config import *
from lib.DBOperate import *
import time
import sqlite3
import threading

def insertOne(file):
    fdata = filedb
    file = file.encode('UTF-8', 'ignore').decode('UTF-8')
    fdata['PATH'] = file
    fdata['Rule_Type'], fdata['Rule_Check'] = setRule(file)
    if not fdata['Rule_Check'] == '':
        fdata = collectFileData(fdata)
        if not fdata == None:
            a = SQLinsert('FILEDB', fdata)
            c.execute(a)

def buildInitDB(allfile):
    for file in allfile:
        insertOne(file)
    # ts = []
    # for file in allfile[:5]:
    #     print(file)
    #     t = threading.Thread(target=insertOne,args=(file,))
    #     t.start()
    #     ts.append(t)
    # for t in ts:
    #     t.join()
    # for i in range(len(allfile)%500):
    #     ts = []
    #     if (i + 1) * 500 < len(allfile):
    #         for file in allfile[i * 500:(i + 1) * 500]:
    #             print(file)
    #             t = threading.Thread(target=insertOne, args=(file))
    #             t.start()
    #             ts.append(t)
    #         for t in ts:
    #             t.join()
    #     else:
    #         for file in allfile[i * 500:]:
    #             t = threading.Thread(target=get_chapter, args=(file))
    #             t.start()
    #             ts.append(t)
    #         for t in ts:
    #             t.join()

if __name__ == '__main__':
    now = time.time()
    connect = sqlite3.connect(initDB_Path)
    c = connect.cursor()
    SQLcreatetable(c,'FILEDB')
    print('新建数据表成功')
    allfile = getDirData()
    buildInitDB(allfile)
    print(time.time()-now)
    connect.commit()
    c.close()
    connect.close()
