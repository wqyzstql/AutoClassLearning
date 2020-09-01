<p align="center">
    <img src="https://i.loli.net/2019/07/22/5d3559f48053594320.png">
</p>

<h1 align="center">AutoWeiBan学习助手</h1>

<div align="center">

辅助麦课安全网课学习

![GitHub release](https://img.shields.io/github/release/WeiYuanStudio/AutoWeiBan.svg?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/WeiYuanStudio/AutoWeiBan.svg?style=flat-square)

</div>

## 2019.10.14紧急修复
**版本92898ced**已经修复了登录问题
官方在近期修改了登录方式，登录请求的POST请求参数被混淆，不知道是官方针对该项目还是仅仅是为了登录安全，反正原帐号密码登录已经失效。  
现已从二维码登录着手，使用微信扫描二维码登录。 

本次更改官方还修改了查询课程进度的接口，返回的JSON键值更改了，本项目也已经跟进修改了JSON解析的键值。经过本人测试，二维码登录未见异常。  
不知道在完成课程请求方面是否有改动，这得靠新号测试才能知道。后期将加入更多的log输出方便用户反馈。若遇到任何问题，请发Issues给我。

**备选方案**。
我的学弟用Java Script开发了一个刷课脚本，如果官方只修改了登录POST请求的话，理论上这个方案也可以的，您可以尝试一下这个方案。
详情访问：

学弟的WBKiller脚本的git仓库地址
<https://git.darc.pro/DarcJC/WBKiller>

使用方法链接位于学弟的个人博客
<https://darc.pro/archives/wbcourse-killer.html>

## 使用方法

1. 首先需要在运行设备上安装Python3运行环境。具体安装方法可以参考网上的教程进行一般操作。或者也可以使用包管理器很方便安装Python（Windows用户可以使用Choco，Mac可以使用Brew，Linux用户，恩，包管理器对于Linux用户来说就是传统艺能）。如果遇到库导入错误，请检查您的Python版本，务必为3

2. 接着打开命令行操作界面，CD（Change Directory）到该脚本的目录下

3. 最后执行`python main.py` 或者 `python3 main.py`即可开始运行该脚本，按照指示使用即可。

## 可以自定义的地方

1. 院校码，这个没有深入研究如何获取到具体学校的tenantCode(院校码，用于发送请求时区分学校)。每个学校的都是不同的，如果你想获取自己学校的tenantCode的话，你可以自己试着登录一次，在浏览器开发者工具中的网络选项卡中查看网络请求信息抓取。或者实在不会操作可以提个Issues过来。（现已加入TODO，该信息可以在登录页面中请求到一个巨大的JSON）

2. 课程间的延迟时间，在**WeiBanAPI.py文件**的头部中有两个参数分别为**baseDelayTime**基础延时秒数和**randomDelayDeviation**叠加随机延时差。**实际延迟时间 = 基础延时秒数 + 叠加随机延时差**
