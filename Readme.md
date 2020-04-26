# 搜狗词库爬虫(sougou_dict_spider)
[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)

> 把人类从重复的劳动中解放出来，去创造新的事物。


## 简介(Introduction)

搜狗输入法的词库可能是目前比较容易获取的开放下载的中文词库了，其中涵盖的内容也是非常的广泛。
包含如下12个大类：

**城市信息，  自然科学，  社会科学，  工程应用，  农林渔畜，  医学医药，  电子游戏，  艺术设计，  生活百科，  运动休闲，  人文科学，  娱乐休闲**

在这个大类之中还由非常多的小类。如果要去一一手动下载，将花费非常多的时间。

所以这个项目诞生了😋!

## 分析


[Python 搜狗词库的批量下载分析](https://www.quanquanting.com/blog/article/?id=13465787 "Python 搜狗词库的批量下载分析")


## 快速开始(Quick start)

#### 环境要求(Requirements):

* Python 3.x (2.x is not supported)
* requests
* bs4

#### 操作步骤(Steps):

1. Git本项目到您的电脑上，或是直接Fork到您自己的仓库

        git clone https://github.com/StuPeter/Sougou_dict_spider.git

2. 目录结构如下：

        .
        ├── main.py
        ├── SougouSpider.py
        ├── Scel2Txt.py
        ├── requirements.txt
        └── Readme.md
    
    + main.py为主程序，用于下载搜狗词库；
    + SougouSpider.py为解析和下载的类，供main.py调用；
    + Scel2Txt.py为.scel文件转.txt程序；
    
3. 要下载搜狗词库文件，需要先打开 main.py

        # 下载类别
        Categories = ['城市信息:167', '自然科学:1', '社会科学:76', '工程应用:96', '农林渔畜:127', '医学医药:132',
              '电子游戏:436', '艺术设计:154', '生活百科:389', '运动休闲:367', '人文科学:31', '娱乐休闲:403']
        # Scel保存路径
        SavePath = r"f:\Users\Documents\zTemp Files\scel1"
        
        # TXT保存路径
        txtSavePath = r"f:\Users\QQT\Documents\zTemp Files\txt"
        
        # 开始链接
        startUrl = "https://pinyin.sogou.com/dict/cate/index/436"

    + 下载类别：为12个大类，默认就是全下载；如果要选择性下载，就请删掉您不要的类目。请保证每个类目名称冒号后的Id不被删除，否则无法下载哦！
    + Scel保存路径：这个自己指定,下载的默认都是.scel文件无法直接使用；
    + TXT保存路径：这个自己指定；
    + 开始链接：这个建议默认；

4. 如上设置设置完毕后，直接运行main.py即可。ps:由于是单线程下载，可能需要较长时间。

5. 当显示“任务结束...”表示下载和转化完毕，最后的词库文件路径为上面设置的 **txtSavePath**


## 许可(License)
[MIT license](https://github.com/StuPeter/Sougou_dict_spider/blob/master/LICENSE "MIT license")
    


