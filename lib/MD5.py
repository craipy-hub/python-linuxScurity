import stat,os
from hashlib import md5
def calFileMd5_bash(filepath:str):
    try:
        md5 = os.popen('md5sum %s' % filepath).read().replace(' ', '').replace(filepath, '')
        return md5
    except:
        print('md5sum %s' % filepath)
        return ''

def calFileMd5(filepath:str):
    m = md5()
    a_file = open(filepath, 'rb')  # 需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

def calBigFileMd5(filename:str):
    if not os.path.isfile(filename):
        return ''
    myhash = md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def getMD5(path:str,Rule:str,mode):
    if path.startswith('/dev') or path.startswith('/sys') or path.startswith('/proc'):
        return ''
    if not stat.S_ISREG(mode):
        return ''
    for i in 'CSHM':
        if i in Rule:
            return calBigFileMd5(path)
    return ''