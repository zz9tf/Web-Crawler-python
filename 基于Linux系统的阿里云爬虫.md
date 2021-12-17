# 简介

在这个文章里主要记述了我使用阿里云搭配Ubuntu来不停跑python爬虫的长期爬取过程。主要记录了我所遇到的一些问题，以便日
后在遇到后，能及时解决。

### 背景

在之前学过各种爬虫技术后，我搭建了一个python文件去收集某个网站上的股票数据，但我发现我需要长期爬取这个网站的数据，
从而形成有效的数据。虽然Windows系统有将python程序定时启动的方式，但经过尝试并未成功。况且为了实现它的定时启动难道
我要一直运行电脑嘛？这样的操作并不保险。为了能持续稳定不断的实现爬取这个功能，最好的办法就是将它放到某个云端，从而
让我能一直运行这个程序。

![image](https://user-images.githubusercontent.com/77183284/146279197-7e28575b-8873-4619-8ded-269acb5d3673.png)

这里我使用了阿里云，买的是新用户丐中丐版云服务器，主要是错过了双十一（据说打折），然后又不想花多少钱。不论怎样，我
使用了这种模式去尝试云端网络爬虫。一开始使用的是windows，但很快就品尝到了10年前老爷机的酸爽，所以迫不得已，开始使
用linux。

## 关于Linux系统的一些东西

### scp命令行使用问题

scp是一种用于将文件从自己电脑传输到另一个远端电脑，或将远端电脑文件下载到自己电脑的命令。

```
// 上传
scp [file location] [userName@ip:location you want to put your files]
// 下载
scp [userName@ip:location you want to download your files] [file location]
```

我遇到的一个问题是，当我将阿里云系统重置之后，scp需要更新自己的信息。而你会遇到诸如如下的问题。

![image](https://user-images.githubusercontent.com/77183284/146279756-27bdbf1a-3caa-4575-bc79-14d6a3677e1b.png)

解决方法：

```
ssh-keygen -R [your ip]
```

之后scp命令就可以重新使用了。

### screen命令行使用

screen是一个用于维持后台程序运行（保持程序的运行）的终端程序。通过它，我保证了我的python程序可以一直在后台运行。

```
# 这里创建了一个新screen，name是自己定义的一个新screen的名字
screen -S name
```

当我关掉terminal的时候，程序依然会运行。

![image](https://user-images.githubusercontent.com/77183284/146506360-08093e91-815a-41c2-81fe-3903f6bed582.png)


而为了看我自己的screen都有哪些，可以使用下述命令。
```
screen -ls
```
![image](https://user-images.githubusercontent.com/77183284/146507389-529ba0f8-9fe5-4fba-a4ad-dc7af77cc368.png)


我可以通过下面的命令来重新连接自己的程序
```
screen -r num
```
![image](https://user-images.githubusercontent.com/77183284/146507593-a7fdd296-af64-4d01-82d0-dee7a4008d5e.png)

![image](https://user-images.githubusercontent.com/77183284/146507962-c7ff7dae-ecf9-4395-9e6c-9ab896793cfe.png)


在将来我不需要这个screen了之后可以重新连接这个screen，并输入exit来关掉程序。
```
screen -r num
exit
```
![image](https://user-images.githubusercontent.com/77183284/146505907-05de8127-f034-47c1-8846-410e3a9b0f0e.png)

## Linux中文显示【未能成功】

我安装的程序是ubuntu_20_04_x64_20G_alibase_20211123.vhd。之前我已经实现了这个系统的图形界面安装，并且python在里面运行良好，但是可能是因为网络或性能等原因，整个系统非常的卡。所以为了解决这个问题，我希望能在没有图形界面的情况下，安装中文字，从而实现python在ssh下的正常运行。

我首先重新刷新了系统（为了删除图形界面，让系统还原为原始系统）。然后执行以下命令来安装中文包
```
sudo apt-get update
sudo apt-get install language-pack-zh-hans
```

在之后具体参考了下述网站配置环境。
```
https://developer.aliyun.com/article/709977
```
![image](https://user-images.githubusercontent.com/77183284/146603298-099fdc95-aac4-4f25-8441-4045b08dde10.png)

##### 语言环境查看

通过如下命令查看语言环境
```
locale ##这个命令可以看当前安装的语言环境
locale -a ## 这个命令可以看所有可用的语言环境
localectl status ## 看一下当前状态
```


```
sudo locale-gen
sudo locale-gen en_US
sudo locale-gen en_US.UTF-8
```

## 关于程序【具体可以看代码】

这个程序有多个部分，分别是今日日期的获取，判断今日是否是工作日（排出节假日与周末股票不更新的情况），目标网站的爬取（并下载到CVS表格中），将数据分散在以股票为单位的几千个单个股票的CVS表格，以及休眠11个小时50分钟（节省计算资源）。由于之前的Linux上的中文安装不成功，所以我暂时绕开了这部分。之前python程序运行完后一直有乱码，然后我就分析了一下到底原因是啥，后来弄明白是因为python在shell上csv的encoding是按照UTF-8来编写的，cvs的读取时gdk（因为有中文字），所以我强制加了encoding="gdk"来写入csv里面。最终测试成功

### 今日日期的获取

这个没啥好出奇的，用的是datetime包

### 判断今日是否是工作日

这里我爬取了百度搜索中搜索”日历“时产生的接口（这个接口提供了当天所在月的节假日以及工作日情况），并对目标进行了解析，分析了哪里代表节假日以及周末等信息。

https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?tn=wisetpl&format=json&resource_id=39043&query=2021%E5%B9%B41%E6%9C%88&t=1639727803299&cb=op_aladdin_callback1639727803299

### 爬取目标网站

大体跟判断今日是否是工作日方法相似，先是找到网址，然后爬下来数据，再进行内容分析即可。

### 将数据分散

这里我觉得有一个亮点就是我把数据下载下来之后以股票为单位分散在不同的csv文件中。好处有几个，首先4000支股票的信息分散为4000多个文件，这样数据的查询就变得快了很多。第二，单只股票数据的抽调就变快了很多，这样就可以针对单只股票进行更好的研究。

### 休眠
休眠11个小时50分钟来节省计算资源。
