import WeiBanAPI
import json
import time  # time.sleep延时
import os  # 兼容文件系统
import random

tenantCode = '43007012'  # 华中农业大学 院校ID
#tenantCode = '4137011066'  # 烟台大学 院校ID


# 密码登录，已经失效
def pwLogin():
    print(
        '默认院校为烟台大学，ID:' + tenantCode + '\n'
        + '若有需要，请自行抓包获取院校ID修改' + '\n'
    )

    # 登录信息输入
    account = input('请输入账号\n')
    password = input('请输入密码\n')

    # 获取Cookies
    print('\n获取Cookies中')
    cookie = WeiBanAPI.getCookie()
    print('Cookies获取成功')
    time.sleep(2)

    randomTimeStamp = random.randint(1E8, 1E12)
    print('验证码,浏览器打开 https://weiban.mycourse.cn/pharos/login/randImage.do?time=' +
          str(randomTimeStamp))

    verifyCode = input('请输入验证码')

    # 登录请求
    loginResponse = WeiBanAPI.login(
        account, password, tenantCode, randomTimeStamp, verifyCode, cookie)
    return loginResponse


def main():
    # 显示License
    licenseFile = open('.' + os.sep + 'LICENSE', encoding='utf-8')
    print(licenseFile.read())
    licenseFile.close()

    # 登录
    # loginResponse = pwLogin()
    # 补打空cookie
    cookie = ''

    try:
        loginResponse = WeiBanAPI.qrLogin()
        taskResponse = WeiBanAPI.getStudyTask(loginResponse['data']['userId'],
                                              tenantCode,
                                              cookie)
        loginResponse['data']["UserProjectId"] = taskResponse['data']['userProjectId']
    except Exception as e:

        print(e)
        raise("初始化失败！")

    try:
        print('登录成功，userName:' + loginResponse['data']['userName'])
        time.sleep(2)
    except BaseException:
        print('登录失败')
        print(loginResponse)  # TODO: 这里的loginResponse调用没有考虑网络错误等问题
        exit(0)

    # 请求解析并打印用户信息
    try:
        print('请求用户信息')
        stuInfoResponse = WeiBanAPI.getStuInfo(loginResponse['data']['userId'],
                                               tenantCode,
                                               cookie)
        print('用户信息：' + stuInfoResponse['data']['realName'] + '\n'
              + stuInfoResponse['data']['orgName']
              + stuInfoResponse['data']['specialtyName']
              )
        time.sleep(2)

    except BaseException:
        print('解析用户信息失败，将尝试继续运行，请注意运行异常')
    # 请求课程完成进度
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['UserProjectId'],
                                                    tenantCode,
                                                    cookie)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' +
              str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
        time.sleep(2)
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')
    # pdb.set_trace()
    # 请求课程列表
    try:
        getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['UserProjectId'],
                                                        '3',
                                                        tenantCode,
                                                        cookie)
        time.sleep(4)
    except BaseException:
        raise RuntimeError("请求课程列表失败")

    print('解析课程列表并发送完成请求')

    for i in getListCourseResponse['data']:
        print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
        NowClass = WeiBanAPI.GetList(loginResponse['data']['UserProjectId'],
                                     i['categoryCode'],
                                     '3',
                                     tenantCode,
                                     '',
                                     cookie)
        for j in NowClass['data']:
            print('课程内容：' + j['resourceName'] +
                  '\nuserCourseId:' + j['userCourseId'])

            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(
                    loginResponse['data']['UserProjectId'], j['resourceId'], tenantCode)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode, cookie)

                delayInt = WeiBanAPI.getRandomTime()
                print('\n随机延时' + str(delayInt))
                time.sleep(delayInt)


if __name__ == '__main__':
    main()
