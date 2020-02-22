import os
from lib.MD5 import getMD5
def getDirData():
    database = os.walk('/')
    allfile = []
    for root, dir, files in database:
        allfile.extend([os.path.join(root, i) for i in files])
        allfile.append(root)
    return allfile

def collectFileData(fdata:dict):
    try:
        STAT = os.stat(fdata['PATH'], follow_symlinks=False)
        fdata['STAT'] = str(STAT).replace('os.st_result', '')
        fdata['MD5'] = getMD5(fdata['PATH'], fdata['Rule_Check'], STAT.st_mode)
        return fdata
    except Exception as e:
        print(e)
        return None
