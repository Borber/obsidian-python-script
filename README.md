- 202107232305 更新 匹配 ![](url "") 类型 markdown 链接

# 说明

首先,这并不是一个插件,而是基于 `Templater` 插件,的一个小方法而已. 其次我使用的系统是 linux 系统, 不保证 Windows 可以正常使用 (你可以魔改我的代码来适配你的系统). 再次, 为什么要做一个这样的东西,而不用现成的, 因为不够优雅,很多别的工具太繁琐,需要切换应用,输入地址,之类的


# 使用教程

## 准备工作

1. 你需要提前安装的有

    1. 毫无疑问,你需要安装 `Obsidian`  以及 `Templater` 插件 并关闭安全模式,启动插件

    1. `Python 3`  以及 其下的模块 `filetype`  [__filetype官网__](https://github.com/h2non/filetype.py) 

1. 你需要做好的心理准备

    1. 有点耐心

    1. 可能你想离线的网站,这个脚本无法做的, 请带着网址来提issus 我会尽量实现

    1. windows 的特殊性

## 开始安装

### Python脚本

复制下面的代码, 放在一个你喜欢的位置, 但最好不要有中文路径, 会不会出bug 我不知道

```python
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
            # 添加后缀支持 前往 https://github.com/h2non/filetype.py 模仿下面的写法添加支持类型
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
```



`getPath` 和 `getPicName` 分别可以自定义 保存路径 和 文件名字 (不包括后缀)

若想添加更多 图片类型 请查找 `#添加后缀支持` 按照注释修改其下方代码



### Templater 脚本 （Linux）

在 `Templater` 的设置中 开启 「允许系统命令」然后在下方输入 `/bin/bash` 来指定 `shell` 

![](assets/3127f2964fe9f957b0904df7dc544ce000f1 "")



在下方点击 `Add New User Function` 新建一个函数 名字随意(引用为: "fName”) 具体指令如下：

```python
python3 "你保存的python脚本地址" "<% tp.file.path() %>" "你的附件资源库的根目录地址" &
```

据我的观察 只有放在附件资源库的根目录地址下, OB 才会自动刷新, 否则可能需要重启才能建立索引. (当然可能是我观察错了, 以你的实际情况为准)

其中 `"<% tp.file.path() %>"` 是你的目标 MarkDown 文件的地址, 由 `Templater` 提供



接下来在你指定的 `Templater` 的模板文件夹中 新建一个模板, 名字你喜欢就好(引用为 「本地化」), 我使用的是 `图片本地化` 

![](assets/31272bcc961a9c7b3c1c9a28063b5ccd775b "")



在模板中 添加 一条语句:

```javascript
<% tp.user.imageToLocal() %>
```

其中 imageToLocal 可以改成你的 `fName` 即可



### Templater 脚本 （Windows/Mac）

自行解决技术点

1. 调用 `shell` 

1. 后台运行 

    1. linux 这边是一定要后台运行的 否则就会报错, 其他平台可以自己尝试



## 使用

1. 在`Obsidian`中找到你想要本地化图片的笔记, 打开它

1. 按下你设置的 `Templater` 插入模板快捷键 选择 「本地化」 等待几秒钟 就可以了



## 演示视频

https://www.aliyundrive.com/s/DCWjHCSx7Ar



## 维护

完全看心情