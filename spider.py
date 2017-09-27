# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import tool
import os
import myThread

#抓取MM
class Spider:

    #页面初始化
    def __init__(self):
        # self.siteURL = u'http://bakufu.jp/archives/category/%E3%83%91%E3%83%B3%E3%83%81%E3%83%A9%E3%83%BB%E3%81%B5%E3%81%A8%E3%82%82%E3%82%82'
        self.siteURL = u'http://bakufu.jp'
        self.tool = tool.Tool()
        self.threads = []

    #获取索引页面的内容
    def getPage(self,pageIndex):
        url = self.siteURL + "/page/" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    #获取索引界面所有MM的信息，list格式
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<h1 class="entry-title"> <a href="(.*?)" title="(.*?)"',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append([item[0],item[1]])
            print item[1].replace(u"\u3078\u306e\u30d1\u30fc\u30de\u30ea\u30f3\u30af", "")
        return contents

    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('utf-8')

    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        return self.tool.replace(result.group(1))

    #获取页面所有图片
    def getAllImg(self,page):
        pattern = re.compile('<a href="(http://img.bakufu.jp.*?_\d+.jpg)" target="_blank"><img src="')
        images = re.findall(pattern,page)
        return images

    #保存多张写真图片
    def saveImgs(self,images,name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    # 保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    #保存个人简介
    def saveBrief(self,content,name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))


    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
         u = urllib.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         print u"正在悄悄保存她的一张图片为",fileName
         f.close()

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False

    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            #页面的URL
            detailURL = item[0]
            #得到页面代码
            detailPage = self.getDetailPage(detailURL)
            #获取所有图片列表
            images = self.getAllImg(detailPage)
            self.mkdir(item[1])
            #保存图片
            # self.saveImgs(images,item[1])
            thread = myThread.myThread(self.saveImgs, images, item[1])
            thread.start()
            self.threads.append(thread)

    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            self.savePageInfo(i)

#传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = Spider()
spider.savePagesInfo(11,11)
end = False
while not end:
    end = True
    for thread in spider.threads:
        if thread.isAlive():
            end = False
            break