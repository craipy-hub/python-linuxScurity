import grp,pwd
import time
import stat
import os

# 根据 stat中查出的组编号,获取组名称
def linuxGroupInfo(st_gid: int):
    """
    根据 stat中查出的组编号,获取组名称
    :param st_gid: 用户组编号
    :return: str 用户组名称
    """
    try:
        entry = grp.getgrgid(st_gid)
        return entry.gr_name
    except:
        return 'UNKNOWN'

# 根据 stat中查出的用户编号,获取用户名称
def linuxUserInfo(st_uid: int):
    """
    根据 stat中查出的用户编号,获取用户名称
    :param st_uid: 用户ID
    :return: str 用户名称
    """
    try:
        entry = pwd.getpwuid(st_uid)
        return entry.pw_name
    except:
        return 'UNKNOWN'


def formatTime(Time: float):
    return time.strftime("%Y年%m月%d日%H:%M:%S", time.localtime(Time))

def formatMode(mode: int):
    return stat.filemode(mode)

def objectType(mode: int):
    if stat.S_ISDIR(mode):
        return 'Directory'
    elif stat.S_ISREG(mode):
        return 'Regular file'
    elif stat.S_ISLNK(mode):
        return 'Shortcut'
    elif stat.S_ISSOCK(mode):
        return 'Socket'
    elif stat.S_ISFIFO(mode):
        return 'Named pipe'
    elif stat.S_ISBLK(mode):
        return 'Block special device'
    elif stat.S_ISCHR(mode):
        return 'Character special device'

# Linux下,根据设备号,获取设备名称
def linuxDeviceToName(no: int):
    """
    Linux下,根据设备号,获取设备名称
    :param no: 设备编号
    :return: str
    """
    for line in open('/proc/partitions'):
        fields = line.split()
        if 0 in fields and 1 in fields and 3 in fields \
                and int(fields[0]) == os.major(no) \
                and int(fields[1]) == os.minor(no):
            return fields[3]
    return 'unKnown'