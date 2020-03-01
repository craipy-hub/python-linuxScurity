import re
from lib.Config import policyPath
path = policyPath
config = {}
Rules = []
def loadPolTxt(path):
    txt = ''
    with open(path, 'r', encoding='utf-8')as f:
        for line in f:
            if(line.strip().startswith('#')):
                pass
            else:
                txt = txt+line
        f.close()
    return txt

def loadPolVar(txt):
    global config
    globalvartxt = re.compile(r'@@section GLOBAL(.*?)@@section FS')
    try:
        globalvar = globalvartxt.search(txt.replace('\n','')).group(1)
        varname = re.findall(r'(\w*?)=',globalvar.replace(' ',''))
        varvalue = re.findall(r'=(.*?);',globalvar.replace(' ',''))
        for i in range(len(varname)):
            config[varname[i]] = varvalue[i].replace('\"','')
    except:
        pass
    return config


def loadPolRules(txt):
    global Rules
    txt = re.sub('#.*\n', '\n', txt)
    if '@@section FS' in txt:
        txt = re.search('@@section FS(.*)',txt,re.S|re.M).group(1)
    else:
        pass
    # 策略文件中的变量替换
    for globalvar in config:
        txt = txt.replace('$('+globalvar+')',config[globalvar])
    # 策略文件的格式转化
    txt = txt.replace('->',':').replace(';',',').replace('}','},},').replace('{','content:{').replace('(','{').replace(')','').replace('=',':').replace(' ','')
    # 被忽略文件的格式转化
    txt = re.sub('!(.*?),', '\\1:"",', txt, flags=re.S | re.M)
    # 字典的key转换
    txt = re.sub('^([\w\/].*?):','"\\1":',txt,flags=re.S|re.M)
    # 字典的value转换
    txt = re.sub(': *?\+(.+?),',':"+\\1",',txt,flags=re.S|re.M)
    # 数据分割成列表
    Rules = re.findall('{(.*?)},},',txt,flags=re.S|re.M)
    for i in range(len(Rules)):
        Rules[i] = eval('{'+Rules[i]+'}}')
        content = Rules[i]['content']
        for path in content:
            content[path] = checkRules(content[path])
        # print(content)
    return Rules

def loadPol():
    global Rules
    try:
        txt = loadPolTxt(path=path)
        try:
            loadPolVar(txt)
            Rules = loadPolRules(txt)

            return {'code':200,'msg':'打开文件成功','rules':Rules}
        except:
            return {'code': 1002, 'msg': '文件加载格式失败失败'}
    except :
        return {'code':1001,'msg':'打开文件失败'}

def checkRules(rulestr:str):
    check = ''
    ignore = ''
    c = re.findall('\+([abcdgilmnprstuCHMS]+)',rulestr)
    ig = re.findall('-([abcdgilmnprstuCHMS]+)',rulestr)
    for i in c:
        check = check+i
    for i in ig:
        ignore = ignore+i
    for i in ignore:
        if i in check:
            check = check.replace(i,'')
    return check

def setRule(path:str):
    dir = path.split('/')
    pathnew = []
    for Rule in Rules:
        RuleContent = Rule['content']
        for RulePath in RuleContent:
            if RulePath.startswith('r'):
                reRule = re.search("r'(.*?)'",RulePath)
                try:
                    reRule = reRule.group(1)
                except:
                    print('策略文件中正则表达式书写有误->',RulePath)
                    print('正确书写形式->',"r'/home.*'")
                if re.search(reRule,path)!=None:
                    return Rule['rulename'],RuleContent[RulePath]
    for i in range(len(dir)):
        a = '/'
        a = a.join(dir[:i+1])
        if a=='':
            a = '/'
        pathnew.append(a)
    pathnew.reverse()
    for i in pathnew:
        for Rule in Rules:
            if i in Rule['content']:
                return Rule['rulename'],Rule['content'][i]

loadPol()
print('策略文件加载完成')
# print(Rules)
