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

getStudyTaskURL = 'https://weiban.mycourse.cn/pharos/index/getStudyTask.do'  # 请求任务列表URL

getProgressURL = 'https://weiban.mycourse.cn/pharos/project/showProgress.do'  # 请求进度 URL

getListCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'  # 请求课程种类 URL

getListURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do'  # 请求课程列表URL

finishCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'  # 请求完成课程URL

getRandImageURL = 'https://weiban.mycourse.cn/pharos/login/randImage.do'  # 验证码URL

doStudyURL = 'https://weiban.mycourse.cn/pharos/usercourse/study.do'  # 学习课程URL

# 获取验证码以及验证码ID URL
genQRCodeURL = 'https://weiban.mycourse.cn/pharos/login/genBarCodeImageAndCacheUuid.do'

# 用于二维码登录刷新登录状态
loginStatusURL = 'https://weiban.mycourse.cn/pharos/login/barCodeWebAutoLogin.do'


def req(url: str, method: str = "POST", param: dict = None):
    data = None
    if param is not None:
        if method == "POST":
            data = bytes(parse.urlencode(param), encoding='utf-8')
        elif method == "GET":
            url = url + "?" + parse.urlencode(param)
        else:
            raise ValueError("Method {} not supported".format(method))

    reqst = request.Request(url=url, data=data, method=method)
    responseStream = request.urlopen(reqst)
    responseText = responseStream.read().decode('utf-8')
    try:
        responseJSON = json.loads(responseText)
        return responseJSON
    except:
        print(responseText)
        return None


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
    return req(getNameURL, "POST", param)

# 获取任务(userProjectId)


def getStudyTask(userId, tenantCode, cookie):
    logger("开始请求用户任务")
    param = {
        'userId': userId,
        'tenantCode': tenantCode
    }
    return req(getStudyTaskURL, "POST", param)


# 获取课程进度
def getProgress(userProjectId, tenantCode, cookie):
    param = {
        'userProjectId': userProjectId,
        'tenantCode': tenantCode
    }
    return req(getProgressURL, "POST", param)


# 获取课程列表
def getListCourse(userProjectId, chooseType, tenantCode, cookie):
    param = {
        'userProjectId': userProjectId,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
    }
    return req(getListCourseURL, "POST", param)


def GetList(userProjectId,  categoryCode, chooseType, tenantCode, name, cookie):
    param = {
        'userProjectId': userProjectId,
        'categoryCode': categoryCode,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
        'name': name
    }
    return req(getListURL, "POST", param)

# 完成课程请求


def finishCourse(userCourseId, tenantCode, cookie):
    param = {
        'userCourseId': userCourseId,
        'tenantCode': tenantCode,
    }
    return req(finishCourseURL, "GET", param)


def getRandomTime():
    return baseDelayTime + random.randint(0, randomDelayDeviation)


def doStudy(userProjectId, userCourseId, tenantCode):
    param = {
        'userProjectId': userProjectId,
        'courseId': userCourseId,
        'tenantCode': tenantCode
    }
    return req(doStudyURL, "POST", param)


# 获取并返回QRCode 链接以及 QRCode ID
def getQRCode():
    rsp = req(genQRCodeURL, "POST")
    logger('Response:' + json.dumps(rsp))
    print('请浏览器打开下面的二维码登录链接，使用二维码登录（若无法登录请检查是否已经在网页端绑定微信登录功能）')
    print(rsp['data']['imagePath'] + '\n')
    return rsp['data']['barCodeCacheUserId']


# 用于二维码登录，刷新是否已经成功登录
def getLoginStatus(qrCodeID):
    param = {
        'barCodeCacheUserId': qrCodeID
    }
    rsp = req(loginStatusURL, "POST", param)
    logger('Response:' + json.dumps(rsp))
    return json.dumps(rsp)


def logger(str):
    print('log >>> ' + str)
