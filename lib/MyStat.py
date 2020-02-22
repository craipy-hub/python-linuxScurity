import re
from lib.FormatInfo import *
StatMap={
    'p':'st_mode',
    'i':'st_ino',
    'n':'st_nlink',
    'a':'st_atime',
    'm':'st_mtime',
    'c':'st_ctime',
    's':'st_size',
    'u':'st_uid',
    'g':'st_gid',
    'd':'st_dev',
    't':'st_type'
}
class Mystat(tuple):
    def __init__(self,str:str):
        self.st_mode = re.search('st_mode=(\d+)',str).group(1)
        self.st_ino = re.search('st_ino=(\d+)',str).group(1)
        self.st_nlink = re.search('st_nlink=(\d+)',str).group(1)
        self.st_atime = re.search('st_atime=(\d+)',str).group(1)
        self.st_mtime = re.search('st_mtime=(\d+)',str).group(1)
        self.st_ctime = re.search('st_ctime=(\d+)',str).group(1)
        self.st_size = re.search('st_size=(\d+)',str).group(1)
        self.st_uid = re.search('st_uid=(\d+)',str).group(1)
        self.st_gid = re.search('st_gid=(\d+)',str).group(1)
        self.st_dev = re.search('st_dev=(\d+)',str).group(1)
        self.st_type = objectType(int(self.st_mode))

class MystatFormated(tuple):
    def __init__(self,str:str):
        self.st_mode = re.search('st_mode=(\d+)',str).group(1)
        self.st_type = objectType(int(self.st_mode))
        self.st_mode = formatMode(int(self.st_mode))

        self.st_ino = re.search('st_ino=(\d+)',str).group(1)
        self.st_nlink = re.search('st_nlink=(\d+)',str).group(1)

        self.st_atime = re.search('st_atime=(\d+)',str).group(1)
        self.st_atime = formatTime(int(self.st_atime))

        self.st_mtime = re.search('st_mtime=(\d+)',str).group(1)
        self.st_mtime = formatTime(int(self.st_mtime))

        self.st_ctime = re.search('st_ctime=(\d+)',str).group(1)
        self.st_ctime = formatTime(int(self.st_ctime))

        self.st_size = re.search('st_size=(\d+)',str).group(1)

        self.st_uid = re.search('st_uid=(\d+)',str).group(1)
        self.st_uid = linuxUserInfo(int(self.st_uid))

        self.st_gid = re.search('st_gid=(\d+)',str).group(1)
        self.st_gid = linuxGroupInfo(int(self.st_gid))

        self.st_dev = re.search('st_dev=(\d+)',str).group(1)
        # self.st_dev = linuxDeviceToName(int(self.st_dev))



