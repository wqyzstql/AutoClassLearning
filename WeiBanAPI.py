from urllib import request, parse
import http.cookiejar
import json
import random
import time

baseDelayTime = 1  # 基础延时秒数

randomDelayDeviation = 1  # 叠加随机延时差

getCookiesURL = 'https://weiban.mycourse.cn/#/login'  # 请求Cookies URL

loginURL = 'https://weiban.mycourse.cn/pharos/login/login.do'  # 登录请求 URL

getNameURL = 'https://weiban.mycourse.cn/pharos/my/getInfo.do'  # 请求姓名 URL

getProgressURL = 'https://weiban.mycourse.cn/pharos/project/showProgress.do'  # 请求进度 URL

getListCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'  # 请求课程种类 URL

getListURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do' # 请求课程列表URL

finishCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'  # 请求完成课程URL

getRandImageURL = 'https://weiban.mycourse.cn/pharos/login/randImage.do'  # 验证码URL

doStudyURL = 'https://weiban.mycourse.cn/pharos/usercourse/study.do'  # 学习课程URL

genQRCodeURL = 'https://weiban.mycourse.cn/pharos/login/genBarCodeImageAndCacheUuid.do'  # 获取验证码以及验证码ID URL

loginStatusURL = 'https://weiban.mycourse.cn/pharos/login/barCodeWebAutoLogin.do'  # 用于二维码登录刷新登录状态


# 获取一个新Cookie
def getCookie():
    cookie = http.cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    return cookie


# 登录请求 已经失效
def login(keyNumber, password, tenantCode, randomTimeStamp, verifyCode, cookie):
    param = {
        'keyNumber': keyNumber,
        'password': password,
        'tenantCode': tenantCode,
        'time': randomTimeStamp,
        'verifyCode': verifyCode
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=loginURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    responseJSON = json.loads(responseText)
    return responseJSON


def qrLogin():
    qrCodeID = getQRCode()
    print(qrCodeID)
    while True:
        responseText = getLoginStatus(qrCodeID)
        responseJSON = json.loads(responseText)
        if responseJSON['code'] == '0':
            return responseJSON
        else:
            print('未登录，等待后5s刷新')
            time.sleep(5)


# 获取学生信息
def getStuInfo(userId, tenantCode, cookie):
    logger('开始请求用户数据')
    param = {
        'userId': userId,
        'tenantCode': tenantCode
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=getNameURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    logger(responseText)
    responseJSON = json.loads(responseText)
    return responseJSON


# 获取课程进度
def getProgress(userProjectId, tenantCode, cookie):
    param = {
        'userProjectId': userProjectId,
        'tenantCode': tenantCode
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=getProgressURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    responseJSON = json.loads(responseText)
    return responseJSON


# 获取课程列表
def getListCourse(userProjectId, chooseType, tenantCode, cookie):
    param = {
        'userProjectId': userProjectId,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=getListCourseURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    responseJSON = json.loads(responseText)
    return responseJSON

def GetList(userProjectId,  categoryCode ,chooseType, tenantCode, name, cookie):
    param = {
        'userProjectId': userProjectId,
        'categoryCode': categoryCode,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
        'name': name
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=getListURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    responseJSON = json.loads(responseText)
    return responseJSON

# 完成课程请求
def finishCourse(userCourseId, tenantCode, cookie):
    param = {
        'userCourseId': userCourseId,
        'tenantCode': tenantCode,
    }
    url_values = parse.urlencode(param)  # GET请求URL参数
    req = request.Request(url=finishCourseURL + '?' + url_values, method='GET')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    print(responseText)


def getRandomTime():
    return baseDelayTime + random.randint(0, randomDelayDeviation)


def doStudy(userProjectId, userCourseId, tenantCode):
    param = {
        'userProjectId': userProjectId,
        'courseId': userCourseId,
        'tenantCode': tenantCode
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=doStudyURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    print(responseText)
    return


# 获取并返回QRCode 链接以及 QRCode ID
def getQRCode():
    req = request.Request(url=genQRCodeURL, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    responseJSON = json.loads(responseText)
    logger('Response:' + responseText)
    print('请浏览器打开下面的二维码登录链接，使用二维码登录（若无法登录请检查是否已经在网页端绑定微信登录功能）')
    print(responseJSON['data']['imagePath'] + '\n')
    return responseJSON['data']['barCodeCacheUserId']


# 用于二维码登录，刷新是否已经成功登录
def getLoginStatus(qrCodeID):
    param = {
        'barCodeCacheUserId': qrCodeID
    }
    data = bytes(parse.urlencode(param), encoding='utf-8')
    req = request.Request(url=loginStatusURL, data=data, method='POST')
    responseStream = request.urlopen(req)
    responseText = responseStream.read().decode('utf-8')
    logger('Response:' + responseText)
    return responseText


def logger(str):
    print('log >>> ' + str)
