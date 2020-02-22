import socket
import getpass
def getHostIp():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

def getUser():
    return getpass.getuser()  # 获取当前用户名

def getHostName():
    return socket.gethostname()