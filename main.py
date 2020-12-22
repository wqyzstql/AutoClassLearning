import WeiBanAPI
import json
import time  # time.sleep延时
import os  # 兼容文件系统
import random

tenantCode = '233333'  # 院校ID


def main():
    loginResponse = WeiBanAPI.qrLogin()

    try:
        print('登录成功，userName:' + loginResponse['data']['userName'])
    except BaseException:
        print('登录失败')
        print(loginResponse)  # TODO: 这里的loginResponse调用没有考虑网络错误等问题
        exit(0)

    # 请求解析并打印用户信息
    try:
        print('请求用户信息')
        stuInfoResponse = WeiBanAPI.getStuInfo(loginResponse['data']['userId'],
                                               tenantCode)
        print('用户信息：' + stuInfoResponse['data']['realName'] + '\n'
              + stuInfoResponse['data']['orgName']
              + stuInfoResponse['data']['specialtyName']
              )
    except BaseException:
        print('解析用户信息失败，将尝试继续运行，请注意运行异常')

    # 请求课程完成进度
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['normalUserProjectId'],
                                                    tenantCode)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' + str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')

    # 请求课程列表
    try:
        getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['normalUserProjectId'],
                                                        '3',
                                                        tenantCode)
    except BaseException:
        print('请求课程列表失败')

    print('解析课程列表并发送完成请求')

    for i in getListCourseResponse['data']:
        print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
        NowClass = WeiBanAPI.GetList(loginResponse['data']['normalUserProjectId'],
                                                        i['categoryCode'],
                                                        '3',
                                                        tenantCode,
                                                        '')
        for j in NowClass['data']:
            print('课程内容：' + j['resourceName'] + '\nuserCourseId:' + j['userCourseId'])

            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(loginResponse['data']['normalUserProjectId'], j['resourceId'], tenantCode)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode)
    print("✔✔✔必修课已完成✔✔✔")
    #选修课
    print("匹配课程开始！")
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['normalUserProjectId'],
                                                    tenantCode)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' + str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')

    # 请求课程列表
    try:
        getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['normalUserProjectId'],
                                                        '1',
                                                        tenantCode)
    except BaseException:
        print('请求课程列表失败')

    print('解析课程列表并发送完成请求')

    for i in getListCourseResponse['data']:
        print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
        NowClass = WeiBanAPI.GetList(loginResponse['data']['normalUserProjectId'],
                                                        i['categoryCode'],
                                                        '1',
                                                        tenantCode,
                                                        '')
        for j in NowClass['data']:
            print('课程内容：' + j['resourceName'] + '\nuserCourseId:' + j['userCourseId'])

            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(loginResponse['data']['normalUserProjectId'], j['resourceId'], tenantCode)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode)
    print("✔✔✔匹配课已完成✔✔✔")
    print("选修课开始！")
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['normalUserProjectId'],
                                                    tenantCode)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' + str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')

    # 请求课程列表
    try:
        getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['normalUserProjectId'],
                                                        '2',
                                                        tenantCode)
    except BaseException:
        print('请求课程列表失败')

    print('解析课程列表并发送完成请求')

    for i in getListCourseResponse['data']:
        print('\n----章节码：' + i['categoryCode'] + '章节内容：' + i['categoryName'])
        NowClass = WeiBanAPI.GetList(loginResponse['data']['normalUserProjectId'],
                                                        i['categoryCode'],
                                                        '2',
                                                        tenantCode,
                                                        '')
        for j in NowClass['data']:
            print('课程内容：' + j['resourceName'] + '\nuserCourseId:' + j['userCourseId'])

            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(loginResponse['data']['normalUserProjectId'], j['resourceId'], tenantCode)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode)
    print("✔✔✔选修课已完成✔✔✔")
if __name__ == '__main__':
    main()
