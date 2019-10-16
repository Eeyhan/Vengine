# Vengine，影擒，专业的影视擒拿手

* 一个极简，清爽，无广告，永久免费的视频资源搜索站，智能自动获取互联网资源，整个平台以restful规范做的前后端分离

## 注意：

### 1.不提供数据和爬虫部分的代码，自行准备

### 2.数据来源于互联网，不提供播放功能，搜索结果是第三方的视频播放链接 ，其中结果如含有广告，请勿轻信，谨防上当

### 3.更多说明代码有注释


## 开发环境


* django2
* python3
* Jqueryo
* djangorestframework
* djang-apscheduler
* mysql
* redis
* bootstrap


## 功能简介：

+ 利用django+djangorestframework搭建的一个前后端分离平台，只提供视频搜索功能，当用户搜索词汇无结果时，记录该搜索词汇存入redis数据库，利用django_apscheduler设定定时任务，设定在每天的凌晨1点30自动获取数据
+ 前端采用bootstrap搭建的一个响应式的页面，与后台做搜索交互，数据实时渲染


## 更新进度

### 2019/10/16号更新：

* 项目已上线，访问地址 https://eeyhan.github.io



## 使用步骤

* 1. 进入根目录，安装需要的库即可 pip install -r requirements.txt

* 2. 自行配置数据库（mysql，redis）
   
* 3. 启动项目即可，Python manage.py runserver [addr:port]
   
## 启动界面

![影擒，专业的影视擒拿手](https://raw.githubusercontent.com/Eeyhan/pictures/master/video1.png)
![影擒，专业的影视擒拿手](https://raw.githubusercontent.com/Eeyhan/pictures/master/video2.png)
![影擒，专业的影视擒拿手](https://raw.githubusercontent.com/Eeyhan/pictures/master/video3.png)
![影擒，专业的影视擒拿手](https://raw.githubusercontent.com/Eeyhan/pictures/master/video4.png)
![影擒，专业的影视擒拿手](https://raw.githubusercontent.com/Eeyhan/pictures/master/video5.png)


### 支持二次开发，二次开发中者请遵守相关法律法规，否则后果自负

## 更多技能点：

### [我的博客](https://www.cnblogs.com/Eeyhan '博客')


   