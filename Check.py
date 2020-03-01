import sqlite3
from lib.Config import *
from lib.DBOperate import *
from lib.Policy import setRule
from lib.FileOperate import *
from lib.MyStat import *
from PrintReport import pReport
import time

def checkChange(allfile):
    for file in allfile:
        fdata = filedb
        file = file.encode('UTF-8', 'ignore').decode('UTF-8')
        fdata['PATH'] = file
        fdata['Rule_Type'], fdata['Rule_Check'] = setRule(file)
        if not fdata['Rule_Check'] == '':
            a = queryFileData(c, 'FILEDB', fdata['PATH'])
            if a==None:             #不在initdb中
                fdata = collectFileData(fdata)
                if not fdata == None:
                    if 'l' not in fdata['Rule_Check']:
                        fdata['Record']='a'
                        print('新增文件：', fdata['PATH'])
                        c.execute(SQLinsert('FILEDB',fdata))
                    else:
                        fdata['Record'] = 'c'
                        c.execute(SQLinsert('FILEDB', fdata))

            else:
                flag = 1
                fdata = collectFileData(fdata)
                if not fdata==None:
                    originStat = Mystat(a[1]).__dict__      #获取原始的stat
                    newStat = Mystat(fdata['STAT']).__dict__        #刚获取的stat
                    for i in fdata['Rule_Check']:
                        if i in StatMap:
                            if originStat[StatMap[i]]!=newStat[StatMap[i]]:
                                print('被修改的文件：',fdata['PATH'])
                                fdata['Record']='m'
                                c.execute(SQLupdate('FILEDB',fdata['PATH'],fdata))
                                flag=0
                                break
                        if i in 'CMHS':
                            if a[2]!=fdata['MD5']:
                                print('MD5被修改的文件：', fdata['PATH'])
                                fdata['Record'] = 'm'
                                c.execute(SQLupdate('FILEDB', fdata['PATH'], fdata))
                                flag = 0
                                break
                    if flag:
                        fdata['Record']='c'
                        c.execute(SQLupdate('FILEDB', fdata['PATH'], fdata))
    SQLQuery = "DELETE FROM FILEDB WHERE Record='c'"
    c.execute(SQLQuery)

if __name__ == '__main__':
    now = time.time()
    checkDBName = formatTime(now)+'.db'
    checkTxtName = formatTime(now)+'.txt'
    checkDBPath = os.path.join(dataDir,checkDBName)
    checkTxtPath = os.path.join(dataDir,checkTxtName)

    if os.path.exists(checkDBPath):
        os.remove(checkDBPath)
    cpcmd = 'cp '+ initDB_Path +' '+checkDBPath
    os.popen(cpcmd)
    print('数据库创建成功')
    connect = sqlite3.connect(checkDBPath)
    c = connect.cursor()
    allfile = getDirData()
    checkChange(allfile)
    print(time.time()-now)
    connect.commit()
    connect.execute("VACUUM")
    c.close()
    connect.close()
    pReport(checkDBPath,checkTxtPath)


