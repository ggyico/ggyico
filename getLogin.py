import requests
import json

# 截取URL中的token
def geturltoken(urldata1):  # s是要处理的字符串
    s = urldata1.split('%26refreshtoken')[0]
    str = "accesstoken%3D"
    n = s[s.index(str) + 14:]
    return n
def getLogin():

    # 获取Token
    s = requests.session()

    username = "193053061"

    password = "Lm1556793231"

    data1 = "username=" + username + "&password=" + password + "&appId=com.supwisdom.jvtc&geo=&deviceId=Yodoy0RJlt0DAGLPCS06Djx9&osType=android"

    url1 = "https://token.jvtc.jx.cn/password/passwordLogin?" + data1

    spot = s.post(url=url1)

    idToken = spot.json()['data']['idToken']

    print(idToken)

    # 获取SESSIONID
    #
    headers = {
        'x-id-token':idToken
    }

    testurl = "https://sso.jvtc.jx.cn/cas/login?service=https%3A%2F%2Fmicroserver4.jvtc.jx.cn%2Fcas%2Floginapp%3FtargetUrl%3Dservice%252Fsignin%252Fxqindex"

    pos = s.get(url=testurl,headers=headers,allow_redirects=False)

    location = pos.headers['Location']

    print(location)

    ticket = s.get(url=location,headers=headers,allow_redirects=False)


    pos2 = ticket.headers['Set-Cookie'].split(";")[0]

    print(pos2)

    urldata = 'https://microserver4.jvtc.jx.cn/cas/loginapp?targetUrl=service%2Fsignin%2Fxqindex'

    userdata = s.get(url=urldata,headers=headers,allow_redirects=False)

    urldata1 = userdata.headers['Location']

    accesstoken = geturltoken(urldata1)

    # 获取打卡信息

    urldaka = 'https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getlxdk'

    headers2 = {

        'Authorization': 'Basic YXBwOmFwcF9zZWNyZXQ=',
        'Content-Type': 'application/json;charset=UTF-8',

    'Blade-Auth': 'bearer '+accesstoken,
    }

    most = s.get(url=urldaka,headers=headers2)

    print(most.text)

    # 最后一步，打卡！！！！
    data2 = {
        "jzqk": "3", "schsjcrq": "0", "hsbg": "null", "dqqdw": "0", "drzt": "", "stzk": "0", "stzkxq": "", "sfmj": "0",
         "sfmjxq": "", "sfscgfxdq": "0", "sfscgfxdqxq": "", "gfxljs": "0", "wzsfbd": "0", "bdfs": "0", "cc": "",
         "ccpz": "null", "bdqswz": "", "bdjswz": "", "location": "江西省九江市濂溪区S22都九高速845号靠近九江职业技术学院濂溪校区-学生宿舍11栋",
         "address": "江西省九江市濂溪区S22都九高速845号靠近九江职业技术学院濂溪校区-学生宿舍11栋", "xgh": "193053061", "gfxljsxq": ""
    }

    urldakalast = 'https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/submit'

    json1 = json.dumps(data2)

    last = s.post(url=urldakalast,data=json1,headers=headers2)

    print(last.text)
getLogin()
