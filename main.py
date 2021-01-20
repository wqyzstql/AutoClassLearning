# -*- coding: utf-8 -*-
import WeiBanAPI

# 院校 ID
tenantCode = '4137011066'


def main():
	worker = WeiBanAPI.WeiBan(tenantCode)
	
	try:
		worker.qrLogin()
		print('登录成功，用户名：' + worker.username)
		worker.printUserInfo()
		worker.printProgress()
		print('解析课程列表并发送完成请求...')
		worker.finishAll()
		print('所有课程已全部完成！')
	except WeiBanAPI.RE as err:
		print(err.reason)
		exit(1)
	except Exception as err:
		print('出现错误：')
		print(err)
		exit(1)
	
	return


if __name__ == '__main__':
	main()
