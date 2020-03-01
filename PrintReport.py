from lib.Config import *
from lib.FormatInfo import *
from lib.MyStat import MystatFormated
import sys, getopt
import sqlite3
from lib.Host import *
from lib.DBOperate import recordmap
import re
import json

from lib.Email import server,mail_content
Objects = {}
RuleHead = ''
def getReportTxt():
    Report = {}
    with open('data/rp', 'r', encoding='utf-8')as f:
        txt = f.read()
        f.close()
    a = re.findall('\(\d-(?P<name>\w+)\)(.*?)\(\d-(?P=name)\)', txt, re.S | re.M)
    for i in a:
        Report[i[0]] = i[1]
    return Report

def getData(datapath):
    global Objects
    connCheck = sqlite3.connect(datapath)
    cCheck = connCheck.cursor()
    connInit = sqlite3.connect(initDB_Path)
    cInit = connInit.cursor()
    cCheck.execute("select Rule_Type from FILEDB group by Rule_Type;")
    Rule_Type = cCheck.fetchall()
    for i in Rule_Type:
        Objects[i[0]]={}
        cCheck.execute("select Record from FILEDB where Rule_Type='%s' group by Record;" % i[0])
        Record = cCheck.fetchall()
        for j in Record:
            Objects[i[0]][j[0]]=[]
            cCheck.execute("select PATH,STAT,MD5 from FILEDB where Rule_Type='%s' and Record='%s'" % (i[0],j[0]))
            Result = cCheck.fetchall()
            for k in Result:
                row = {}
                row['PATH']=k[0]
                row['NEW'] = {}
                row['ORIGIN'] = {}
                if j[0]=='m':
                    row['NEW']['STAT'] = MystatFormated(k[1]).__dict__
                    row['NEW']['MD5'] = k[2]
                    cInit.execute("select STAT,MD5 from FILEDB where PATH='%s'" % row['PATH'])
                    origin = cInit.fetchall()[0]
                    row['ORIGIN']['STAT'] = MystatFormated(origin[0]).__dict__
                    row['ORIGIN']['MD5'] = origin[1]
                elif j[0]=='a':
                    row['NEW']['STAT'] = MystatFormated(k[1]).__dict__
                    row['NEW']['MD5'] = k[2]
                elif j[0]=='o':
                    row['NEW']['STAT'] = MystatFormated(k[1]).__dict__
                    row['NEW']['MD5'] = k[2]
                    row['ORIGIN']['STAT'] = MystatFormated(k[1]).__dict__
                    row['ORIGIN']['MD5'] = k[2]
                Objects[i[0]][j[0]].append(row)
    cInit.close()
    connInit.close()
    cCheck.close()
    connCheck.close()
    # with open('Objects.json','w',encoding='utf-8')as f:
    #     json.dump(Objects,f,ensure_ascii=False,indent=4)
    return Objects

def getReportSummary(ReportSummary):
    username = getUser()
    hostname = getHostName()
    hostip = getHostIp()
    timenow = formatTime(time.time())
    ReportSummary = re.sub('\$\(HName\)', hostname, ReportSummary)
    ReportSummary = re.sub('\$\(HostIP\)', hostip, ReportSummary)
    ReportSummary = re.sub('\$\(user\)', username, ReportSummary)
    ReportSummary = re.sub('\$\(time\)', timenow, ReportSummary)
    # print(ReportSummary)
    return ReportSummary

def getRuleSummary(RuleSummary):
    count = 0
    for i in Objects:
        row =  '  '
        RuleName = i
        # 规则名
        row = row+RuleName.ljust(32, " ")
        # 规则等级
        row = row+'0'.ljust(18,' ')
        if 'a' in Objects[i]:
            l = len(Objects[i]['a'])
            count = count +l
            row = row+str(l).ljust(9,' ')
        else:
            row = row + '0'.ljust(9, ' ')

        if 'o' in Objects[i]:
            l = len(Objects[i]['o'])
            count = count + l
            row = row+str(l).ljust(9,' ')
        else:
            row = row + '0'.ljust(9, ' ')

        if 'm' in Objects[i]:
            l = len(Objects[i]['m'])
            count = count + l
            row = row + str(l).ljust(9, ' ')
        else:
            row = row + '0'.ljust(9, ' ')
        row = row+'\n'
        RuleSummary = RuleSummary+row+'\n'
    RuleSummary = RuleSummary+'Total violations found:' + str(count) + '\n'
    # print(RuleSummary)
    return RuleSummary

def getRuleHead(RuleName):
    return re.sub('\$\(RuleName\)', RuleName, RuleHead, re.M)

def getRuleDetail():
    RulesDetail = ''
    for Rule in Objects:
        group = getRuleHead(Rule)
        for i in Objects[Rule]:
            group = group+recordmap[i]+':\n'
            for j in Objects[Rule][i]:
                row = '"'+j['PATH']+'"\n'
                group = group+row
        RulesDetail = RulesDetail+group
    # print(RulesDetail)
    return RulesDetail

def getChangeDetail(ChangeDetail):
    ChangeDetails = ''
    for Rule in Objects:
        group = getRuleHead(Rule)
        for i in Objects[Rule]:
            for j in Objects[Rule][i]:
                ObjectHeader = re.sub('\$\(PATH\)', j['PATH'], ChangeDetail, re.M)
                ObjectHeader = re.sub('\$\(change\)', recordmap[i], ObjectHeader, re.M)
                group = group + ObjectHeader
                for st in j['NEW']['STAT']:
                    if i =='m':
                        row = '  '+st.ljust(21,' ')+\
                              j['ORIGIN']['STAT'][st].ljust(35,' ')+\
                              j['NEW']['STAT'][st].ljust(35,' ')+'\n'
                    elif i =='a':
                        row = '  ' + st.ljust(21, ' ') + \
                              '---'.ljust(35, ' ') + \
                              j['NEW']['STAT'][st].ljust(35, ' ')+'\n'
                    elif i=='o':
                        row = '  ' + st.ljust(21, ' ') + \
                              j['ORIGIN']['STAT'][st].ljust(35, ' ') + \
                              '---'.ljust(35, ' ')+'\n'
                    group=group+row
                if i == 'm':
                    row = '  ' + 'MD5'.ljust(21, ' ') + \
                          j['ORIGIN']['MD5'].ljust(35, ' ') + \
                          j['NEW']['MD5'].ljust(35, ' ') + '\n'
                elif i == 'a':
                    row = '  ' + 'MD5'.ljust(21, ' ') + \
                          '---'.ljust(35, ' ') + \
                          j['NEW']['MD5'].ljust(35, ' ') + '\n'
                elif i == 'o':
                    row = '  ' + 'MD5'.ljust(21, ' ') + \
                          j['ORIGIN']['MD5'].ljust(35, ' ') + \
                          '---'.ljust(35, ' ') + '\n'
                group = group + row
        ChangeDetails = ChangeDetails + group
    # print(ChangeDetails)
    return ChangeDetails


def printReport(output_file):
    global RuleHead
    Report = getReportTxt()
    RuleHead = Report['RuleHead']
    Report['ReportSummary'] = getReportSummary(Report['ReportSummary'])
    Report['RuleSummary'] = getRuleSummary(Report['RuleSummary'])
    Report['RuleDetail'] = getRuleDetail()
    Report['ChangeDetail'] = getChangeDetail(Report['ChangeDetail'])
    ReportTxt = Report['ReportSummary']+Report['RuleSummary']+Report['RuleDetail']+Report['ChangeDetail']
    with open(output_file,'w',encoding='utf-8')as f:
        f.write(ReportTxt)
        f.close()
    # return ReportTxt
def sendReport(output_file):
    if os.stat(output_file).st_size>1024*1024*5:
        mail_content['content_text'] = '有较多的文件被修改，请尽快登陆服务器查看报告'
        server.send_mail(['cpy_3566@163.com'], mail_content)
    else:
        mail_content['attachments'].append(output_file)
        server.send_mail(['cpy_3566@163.com'], mail_content)

def pReport(input,out):
    getData(input)
    printReport(out)
    sendReport(out)
if __name__ == '__main__':
    # opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    # input_file = ""
    # output_file = ""
    # for op, value in opts:
    #     if op == "-i":
    #         input_file = value
    #     elif op == "-o":
    #         output_file = value
    #     elif op == "-h":
    #         print('暂时没有帮助文档，请前往https://github.com/binfengxueqian/python-linuxScurity')
    #         sys.exit()
    #
    # if not input_file=='':
    #     print('打开文件',input_file)
    # else:
    #     print('请选择要打印的数据库')
    #     sys.exit()
    # if not output_file=='':
    #     print('报告输出至文件',output_file)
    # else:
    #     print('直接输出')
    input_file = dataDir + '/test.db'
    output_file = dataDir + '/test.txt'
    Objects = getData(input_file)
    printReport(output_file)

    if os.stat(output_file).st_size>1024*1024*5:
        mail_content['content_text'] = '有较多的文件被修改，请尽快登陆服务器查看报告'
        server.send_mail(['cpy_3566@163.com'], mail_content)
    else:
        mail_content['attachments'].append(output_file)
        server.send_mail(['cpy_3566@163.com'], mail_content)