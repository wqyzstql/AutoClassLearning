from urllib import parse
import json
import random
import time
import requests
import os

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

getStudyTaskURL = 'https://weiban.mycourse.cn/pharos/index/getStudyTask.do'

# 二维码登录
def qrLogin():
    qrCodeID = getQRCode()
    
    try:
        while True:
            responseText = getLoginStatus(qrCodeID)
            responseJSON = json.loads(responseText)
            if responseJSON['code'] == '0':
                responseInfo = getStudyTask(responseJSON['data']['userId'],responseJSON['data']['tenantCode'])
                responseJSON['data']['normalUserProjectId']=responseInfo['data']['userProjectId']
                return responseJSON
            else:
                print('未登录，等待后5s刷新')
                time.sleep(5)
    except KeyboardInterrupt:
        print('用户中止程序运行')

def getStudyTask(userId, tenantCode):
    print('开始请求最新课程: ')
    param = {
        'userId': userId,
        'tenantCode': tenantCode
    }
    req = requests.post(url=getStudyTaskURL, data=param)
    responseJSON = json.loads(req.text)
    return responseJSON

# 获取学生信息
def getStuInfo(userId, tenantCode):
    print('开始请求用户数据')
    param = {
        'userId': userId,
        'tenantCode': tenantCode
    }
    req = requests.post(url=getNameURL, data=param)
    responseJSON = json.loads(req.text)
    return responseJSON


# 获取课程进度
def getProgress(userProjectId, tenantCode):
    param = {
        'userProjectId': userProjectId,
        'tenantCode': tenantCode
    }
    req = requests.post(url=getProgressURL, data=param)
    responseJSON = json.loads(req.text)
    return responseJSON


# 获取课程列表
def getListCourse(userProjectId, chooseType, tenantCode):
    param = {
        'userProjectId': userProjectId,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
    }
    req = requests.post(url=getListCourseURL, data=param)
    responseJSON = json.loads(req.text)
    return responseJSON

def GetList(userProjectId,  categoryCode ,chooseType, tenantCode, name):
    param = {
        'userProjectId': userProjectId,
        'categoryCode': categoryCode,
        'chooseType': chooseType,
        'tenantCode': tenantCode,
        'name': name
    }
    req = requests.post(url=getListURL, data=param)
    responseJSON = json.loads(req.text)
    return responseJSON

# 完成课程请求
def finishCourse(userCourseId, tenantCode):
    param = {
        'userCourseId': userCourseId,
        'tenantCode': tenantCode,
    }
    url_values = parse.urlencode(param)  # GET请求URL参数
    req = requests.get(url=finishCourseURL + '?' + url_values)
    print(req.text)


def getRandomTime():
    return baseDelayTime + random.randint(0, randomDelayDeviation)


def doStudy(userProjectId, userCourseId, tenantCode):
    param = {
        'userProjectId': userProjectId,
        'courseId': userCourseId,
        'tenantCode': tenantCode
    }
    req = requests.post(url=doStudyURL, data=param)
    print(req.text)
    return


# 获取并返回QRCode 链接以及 QRCode ID
def getQRCode():
    req = requests.post(url=genQRCodeURL)
    responseJSON = json.loads(req.text)
    print('请扫描二维码登录')
    os.system('explorer {}'.format(responseJSON['data']['imagePath']))
    return responseJSON['data']['barCodeCacheUserId']


# 用于二维码登录，刷新是否已经成功登录
def getLoginStatus(qrCodeID):
    param = {
        'barCodeCacheUserId': qrCodeID
    }
    req = requests.post(url=loginStatusURL, data=param)
    return req.text
