# -*- coding: utf-8 -*-
'''
微伴自动做题模块
'''
import requests
import json
import time
import os


class RE(Exception):
	'''
	WeiBan 类自定义运行时错误
	'''
	def __init__(self, reason):
		self.reason = reason


class WeiBan:
	'''
	微伴做题主模块
	'''
	# API 列表
	# 获取验证码以及验证码 ID
	__genQRCodeURL = 'https://weiban.mycourse.cn/pharos/login/genBarCodeImageAndCacheUuid.do'
	
	# 用于二维码登录刷新登录状态
	__loginStatusURL = 'https://weiban.mycourse.cn/pharos/login/barCodeWebAutoLogin.do'
	
	# 请求姓名
	__getNameURL = 'https://weiban.mycourse.cn/pharos/my/getInfo.do'
	
	# 请求当前任务
	__getTaskURL = 'https://weiban.mycourse.cn/pharos/index/getStudyTask.do'
	
	# 请求进度
	__getProgressURL = 'https://weiban.mycourse.cn/pharos/project/showProgress.do'
	
	# 请求课程种类
	__getListCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do'
	
	# 请求课程列表
	__getListURL = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do'
	
	# 请求完成课程
	__finishCourseURL = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do'
	
	# 学习课程
	__doStudyURL = 'https://weiban.mycourse.cn/pharos/usercourse/study.do'
	
	def __init__(self, schoolID):
		self.tenantCode = schoolID
		return
	
	def qrLogin(self):
		'''
		TODO
		'''
		try:
			self.qrCodeID = self.__getQRCode()
			time.sleep(5)
			while True:
				responseText = self.__getLoginStatus()
				responseJSON = json.loads(responseText)
				if responseJSON['code'] == '0':
					self.username = responseJSON['data']['userName']
					self.userID = responseJSON['data']['userId']
					self.__getTask()
					# self.projectID = responseJSON['data']['preUserProjectId']
					# self.projectID = '95bbd1bc-6361-4352-9db5-a5ddf4d347b7'
					break
				else:
					print('未登录，等待后5s刷新')
					time.sleep(5)
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
			
		return
	
	# 获取并返回 QRCode 链接以及 QRCode ID
	def __getQRCode(self):
		try:
			r = requests.post(self.__genQRCodeURL)
			responseJSON = json.loads(r.text)
			
			if os.name == 'nt':
				# Windows 系统直接用 explorer.exe 打开浏览器
				print('请扫描二维码登录')
				os.system('explorer.exe {}'.format(responseJSON['data']['imagePath']))
				print('如浏览器未自动打开，请打开下面的URL并扫描二维码登录')
			else:
				# TODO: Print the QR code in the terminal
				print('请打开下面的URL并扫描二维码登录')
			
			print(responseJSON['data']['imagePath'])
			return responseJSON['data']['barCodeCacheUserId']
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
	
	# 用于二维码登录，刷新是否已经成功登录
	def __getLoginStatus(self):
		try:
			param = {
				'barCodeCacheUserId': self.qrCodeID
			}
			r = requests.post(self.__loginStatusURL, data=param)
			return r.text
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
	
	def printUserInfo(self):
		'''
		打印学生信息
		'''
		param = {
			'userId': self.userID,
			'tenantCode': self.tenantCode
		}
		r = requests.post(self.__getNameURL, data=param)
		info = json.loads(r.text)['data']
		print('用户信息：')
		print(info['realName'], info['orgName'], info['specialtyName'])
		return
	
	def printProgress(self):
		'''
		打印课程进度
		'''
		try:
			param = {
				'userProjectId': self.projectID,
				'tenantCode': self.tenantCode
			}
			r = requests.post(self.__getProgressURL, data=param)
			progress = json.loads(r.text)['data']
			print('课程总数：' + str(progress['requiredNum']))
			print('完成课程：' + str(progress['requiredFinishedNum']))
			print('结束时间：' + str(progress['endTime']))
			print('剩余天数：' + str(progress['lastDays']))
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
		return
	
	# 获取课程列表
	def __getCourseList(self, chooseType):
		param = {
			'userProjectId': self.projectID,
			'chooseType': chooseType,
			'tenantCode': self.tenantCode,
		}
		r = requests.post(self.__getListCourseURL, data=param)
		return json.loads(r.text)['data']
	
	def __getTask(self):
		try:
			param = {
				'userId': self.userID,
				'tenantCode': self.tenantCode
			}
			r = requests.post(self.__getTaskURL, data=param)
			response = json.loads(r.text)
			if response['code'] == '0':
				self.projectID = response['data']['userProjectId']
			else:
				raise RE('请求失败\n' + r.text)
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
		return
	
	def __getList(self, categoryCode, chooseType, name):
		try:
			param = {
				'userProjectId': self.projectID,
				'categoryCode': categoryCode,
				'chooseType': chooseType,
				'tenantCode': self.tenantCode,
				'name': name
			}
			r = requests.post(self.__getListURL, data=param)
			return json.loads(r.text)['data']
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
	
	# 完成课程请求
	def __finishCourse(self, userCourseID):
		try:
			r = requests.get('{}?userCourseId={}&tenantCode={}'.format(self.__finishCourseURL, userCourseID, self.tenantCode))
			print(r.text)
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
		# TODO: Modify so we know if it succeed or not
		return
	
	def __doStudy(self, userCourseId):
		try:
			param = {
				'userProjectId': self.projectID,
				'courseId': userCourseId,
				'tenantCode': self.tenantCode
			}
			r = requests.post(self.__doStudyURL, data=param)
			print(r.text)
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
		return
	
	def finishAll(self):
		'''
		尝试完成所有课程
		'''
		try:
			courses = self.__getCourseList('3')
			
			for course in courses:
				print('章节码：' + course['categoryCode'])
				print('章节内容：' + course['categoryName'])
				classes = self.__getList(course['categoryCode'], '3', '')
				for item in classes:
					print('课程内容：' + item['resourceName'])
					
					if (item['finished'] == 1):
						print('已完成')
					else:
						print('发送完成请求')
						self.__doStudy(item['resourceId'])
						self.__finishCourse(item['userCourseId'])
				print('')
		except KeyboardInterrupt:
			raise RE('用户中止程序运行')
		except requests.exceptions.ConnectionError:
			raise RE('无法连接至服务器：连接故障')
		except requests.exceptions.ConnectTimeout:
			raise RE('无法连接至服务器：请求超时')
		
		return
