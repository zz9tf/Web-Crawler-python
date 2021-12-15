# 简介

在这个文章里主要记述了我使用阿里云搭配Ubuntu来不停跑python爬虫的长期爬取过程。主要记录了我所遇到的一些问题，以便日
后在遇到后，能及时解决。

# 背景

在之前学过各种爬虫技术后，我搭建了一个python文件去收集某个网站上的股票数据，但我发现我需要长期爬取这个网站的数据，
从而形成有效的数据。虽然Windows系统有将python程序定时启动的方式，但经过尝试并未成功。况且为了实现它的定时启动难道
我要一直运行电脑嘛？这样的操作并不保险。为了能持续稳定不断的实现爬取这个功能，最好的办法就是将它放到某个云端，从而
让我能一直运行这个程序。

![image](https://user-images.githubusercontent.com/77183284/146279197-7e28575b-8873-4619-8ded-269acb5d3673.png)

这里我使用了阿里云，买的是新用户丐中丐版云服务器，主要是错过了双十一（据说打折），然后又不想花多少钱。不论怎样，我
使用了这种模式去尝试云端网络爬虫。一开始使用的是windows，但很快就品尝到了10年前老爷机的酸爽，所以迫不得已，开始使
用linux。

# scp命令行使用问题

scp是一种用于将文件从自己电脑传输到另一个远端电脑，或将远端电脑文件下载到自己电脑的命令。

'''
// 上传
scp [file location] [userName@ip:location you want to put your files]
// 下载
scp [userName@ip:location you want to download your files] [file location]
'''

我遇到的一个问题是，当我将阿里云系统重置之后，scp需要更新自己的信息。而你会遇到诸如如下的问题。

![image](https://user-images.githubusercontent.com/77183284/146279756-27bdbf1a-3caa-4575-bc79-14d6a3677e1b.png)

解决方法：

'''
ssh-keygen -R [your ip]
'''

之后scp命令就可以重新使用了。
