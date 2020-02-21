import grp,pwd
import time
import stat

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
