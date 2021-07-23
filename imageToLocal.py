#! /usr/bin env python3
# -- coding:utf-8 --

from urllib import request
import time
import filetype
import uuid
import sys
import re
import os

class ImageTool():

    def __init__(self,file:str, path:str) -> None:
        if not file.endswith(".md") :
            print ('请在 MarkDown文件中使用')
            self.type = False
        else:
            self.type = True

        self.file = file
        if not path.endswith('/'):
            path = path + '/'
        self.path = path

    # 定义保存文件夹名称
    # "%Y-%m-%d %H:%M:%S" 2021-07-22 11:45:39
    def getPath(self) -> str:
        datePath = time.strftime('%Y%m%d', time.localtime())
        mdPath = self.file.rsplit("/")[-1].replace('.md','')
        realPath = self.path + datePath + "/" +  mdPath + "/"
        
        return realPath


    # 定义图片名称逻辑
    def getPicName(self) -> str:
        return str(uuid.uuid4()).replace('-','')


    def imageToLocal(self) -> None:
        all = ''
        with open(self.file, 'r') as f:
            all = f.read()
        urlList = re.findall(r'\!\[.*\]\(.+\)' , all)
        path = self.getPath()
        self.justGiveMeTheFuckingDir(path)
        mkList = []
        obList = []
        count = 0
        for i in range(0,len(urlList)):
            picUrl = urlList[i].replace('![](', '').replace(')','')
            name = self.getPicName()
            with request.urlopen(picUrl) as web:
                # 为保险起见使用二进制写文件模式，防止编码错误
                with open(path + name, 'wb') as outfile:
                    outfile.write(web.read())
            fType = filetype.guess(path + name)
            # 前往 https://github.com/h2non/filetype.py 模仿下面的写法添加支持类型
            suffix = ''
            if fType is None:
                os.remove(path + name)
                continue
            elif fType.mime == 'image/jpeg':
                suffix = 'jpg'
            elif fType.mime == 'image/png':
                suffix = 'png'
            elif fType.mime == 'image/gif':
                suffix = 'gif'
            elif fType.mime == 'image/webp':
                suffix = 'webp'
            os.rename(path + name, path + name + '.' + suffix)
            mkList.append(urlList[i])
            obList.append('![[' + name + '.' + suffix + ']]')
        self.mkList = mkList
        self.obList = obList
    
    # 替换 md 文件 中的图片 url 为 本地链接
    def changeMkToOB(self) -> None:
        file_data = ''
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                file_data += line
        for i in range(0,len(self.mkList)):
            file_data = file_data.replace(self.mkList[i],self.obList[i])
        with open(self.file, "w",encoding="utf-8") as f:
            f.write(file_data)

    def justGiveMeTheFuckingDir(self, dirPath) -> None:
        folder = os.path.exists(dirPath)
        if not folder:
            os.makedirs(dirPath)





if __name__ == '__main__':
    image_t = ImageTool(sys.argv[1],sys.argv[2])
    image_t.imageToLocal()
    image_t.changeMkToOB()
