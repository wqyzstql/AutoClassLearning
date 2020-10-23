import os
import json
import random
import time
import http.cookiejar
from urllib import request, parse

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


def req(url: str, method: str = "POST", param: dict = None, binary=False):
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
    if not binary:
        responseText = responseStream.read().decode('utf-8')
        try:
            responseJSON = json.loads(responseText)
            return responseJSON
        except:
            return responseText
    else:
        return responseStream.read()


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
    logger('请求二维码 Response:' + json.dumps(rsp))
    try:
        import webbrowser
        webbrowser.open_new_tab(rsp['data']['imagePath'])
    except:
        pass
    print('如果浏览器未自动打开，则请手动在浏览器器中打开下面的二维码登录链接，使用二维码登录（若无法登录请检查是否已经在网页端绑定微信登录功能）')
    print(rsp['data']['imagePath'] + '\n')
    return rsp['data']['barCodeCacheUserId']


# 用于二维码登录，刷新是否已经成功登录
def getLoginStatus(qrCodeID):
    param = {
        'barCodeCacheUserId': qrCodeID
    }
    rsp = req(loginStatusURL, "POST", param)
    return json.dumps(rsp)


def logger(str):
    print('log >>> ' + str)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


################################################################################

def main():
    # 显示License
    with open('.' + os.sep + "LICENSE") as f:
        print(f.read())

    # 使用二维码登录
    cookie = ''
    loginResponse = ""
    try:
        loginResponse = qrLogin()
        data = loginResponse['data']
        userId = data['userId']
        userName = data['userName']
        tenantCode = data['tenantCode']
        taskResponse = getStudyTask(userId, tenantCode, cookie)
        userProjectId = taskResponse['data']['userProjectId']
    except Exception as e:
        raise Exception("初始化失败！", loginResponse, "\n", e)
    else:
        print('登录成功\n', loginResponse, "\n")

    # 请求用户信息
    stuInfoResponse = ""
    try:
        print('请求用户信息')
        stuInfoResponse = getStuInfo(userId, tenantCode, cookie)
        print("用户信息\n", stuInfoResponse, "\n")
    except Exception as e:
        raise Exception('解析用户信息失败', stuInfoResponse, "\n", e)

    ProgressResponse = ""
    # 请求课程完成进度
    try:
        ProgressResponse = getProgress(
            userProjectId, tenantCode, cookie)
        print("课程进度信息\n", ProgressResponse, "\n")
    except Exception as e:
        raise Exception('解析课程进度失败', ProgressResponse, "\n", e)

    ListCourseResponse = ""
    # 获取当前学习任务的所有章节
    try:
        ListCourseResponse = getListCourse(
            userProjectId, '3', tenantCode, cookie)
        print("课程信息\n", ListCourseResponse, "\n")
    except Exception as e:
        raise RuntimeError("请求课程列表失败", ListCourseResponse, "\n", e)
    # 遍历每个章节
    for chap in ListCourseResponse['data']:
        code, name = chap['categoryCode'], chap['categoryName']
        print("当前章节", chap, "\n")
        try:
            # 获取该章节内所有课程
            data = GetList(
                userProjectId, code, '3', tenantCode, "", cookie)['data']
            print("该章节课程: \n", len(data))
            for course in data:
                print("---- ", course['resourceName'], end="")
                if course['finished'] == 1:
                    print(bcolors.OKGREEN + '已完成' + bcolors.ENDC)
                else:
                    print("尝试发送已做完请求....", end="")
                    try:
                        doStudy(
                            userProjectId, course['resourceId', tenantCode, cookie])
                        finishCourse(
                            course['userCourseId'], tenantCode, cookie)
                        delayInt = getRandomTime()
                        time.sleep(delayInt)
                    except Exception as e:
                        print(bcolors.WARNING + "尝试失败 " + bcolors.ENDC, e)
                    else:
                        print(bcolors.OKGREEN + "完成该课程" + bcolors.ENDC)
        except Exception as e:
            print("章节", name, "失败!\n", e, "\n")
        else:
            print("章节", name, "成功!")


if __name__ == '__main__':
    main()
