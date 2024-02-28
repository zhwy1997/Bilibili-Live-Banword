# Bilibili-Live-Banword
使用扫码登陆框架，同时管理直播间屏蔽词

## 主要功能
1. 使用GUI管理本地屏蔽词清单  
参考格式为 {"topic1":["word1","word2"]}
每个主题下有复数个屏蔽词组成的屏蔽词列表，主题之间屏蔽词列表允许重复。
2. 选择复数个主题，添加到/移除自 直播间  
先根据选择的主题生成不重复的屏蔽词列表，再循环执行bilibili添加/移除屏蔽词的api

## 使用指南
1. 管理屏蔽词清单  
点击本地屏蔽词清单，管理本地的屏蔽词，在子窗口编辑完成后点击【保存当前列表到本地】
清单存储于wordlist.json
保存之后下次再开启仍然生效

2. 登录  
点击登录按钮会出现二维码，这时候窗口可能会卡死，扫码登录等待5秒就会重新刷新窗口状态。
曲奇会存放在本地的cookie.txt文件中
二维码也会存放在本地的qr.png中。

3. 选择屏蔽词，填写房间号  
选择复数个主题，生成屏蔽词清单。同时填写房间号。两者都有值时点击【添加到直播间】/【从直播间移除】按钮

4. 输出结果  
结果输出在右侧窗口，同时存放在本地logging.log文件

## 其他说明
python随便写写，gui毫无设计感，能用就行。  
网络异常部分都没做异常处理，不排除当前版本发送请求时报错崩溃。  
(python开启代理请求时容易发生这类问题，也没做处理)  
## 项目引用
根据[@zer0e](https://github.com/zer0e/Bilibili-Api-Framework)的代码重写而成  
主要使用其 bilibiliQRLogin.py 用于二维码登录

API参考  
@SocialSisterYi [哔哩哔哩-API收集整理](https://github.com/SocialSisterYi/bilibili-API-collect)

## 项目依赖
requests  
websocket-client  
qrcode  
PIL  