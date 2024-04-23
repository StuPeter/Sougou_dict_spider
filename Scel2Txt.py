#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2018/8/17
# @Author  : 圈圈烃
# @File    : Scel2Txt.py
# @Description:
# 将搜狗的词库.scel文件转化为.txt文件
# 本人在之前作者的基础上进行了部分修改
# 添加了单个文件转化函数single_file()
# 添加了多个文件转化函数batch_file()
#
############################################################################
# 第二作者
# 由于原代码不适用python3且有大量bug
# 以及有函数没有必要使用且一些代码书写不太规范或冗余
# 所以本人在原有的大框架基本不动的情况下作了大量的细节更改
# 使得没有乱码出现，文件夹导入更方便等等
# Author：Ling Yue, Taiyuan U of Tech
# Blog: http://blog.yueling.me
############################################################################
# 第一原作者：
# 搜狗的scel词库就是保存的文本的unicode编码，每两个字节一个字符（中文汉字或者英文字母）
# 找出其每部分的偏移位置即可
# 主要两部分
# 1.全局拼音表，貌似是所有的拼音组合，字典序
#       格式为(index,len,pinyin)的列表
#       index: 两个字节的整数 代表这个拼音的索引
#       len: 两个字节的整数 拼音的字节长度
#       pinyin: 当前的拼音，每个字符两个字节，总长len
#
# 2.汉语词组表
#       格式为(same,py_table_len,py_table,{word_len,word,ext_len,ext})的一个列表
#       same: 两个字节 整数 同音词数量
#       py_table_len:  两个字节 整数
#       py_table: 整数列表，每个整数两个字节,每个整数代表一个拼音的索引
#
#       word_len:两个字节 整数 代表中文词组字节数长度
#       word: 中文词组,每个中文汉字两个字节，总长度word_len
#       ext_len: 两个字节 整数 代表扩展信息的长度，好像都是10
#       ext: 扩展信息 前两个字节是一个整数(不知道是不是词频) 后八个字节全是0
#
#      {word_len,word,ext_len,ext} 一共重复same次 同音词 相同拼音表
#############################################################################
import struct
import os

# 拼音表偏移
startPy = 0x1540;

# 汉语词组表偏移
startChinese = 0x2628;


def byte2str(data):
    """
    原始字节码转为字符串
    """
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0])
        if c != chr(0):
            str += c
        pos += 2
    return str


def getPyTable(data, GPy_Table):
    """
    获取拼音表
    """
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        lenPy = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        py = byte2str(data[pos:pos + lenPy])

        GPy_Table[index] = py
        pos += lenPy


def getWordPy(data, GPy_Table):
    """
    获取一个词组的拼音
    """
    pos = 0
    ret = ''
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        ret += "'" + GPy_Table[index]
        pos += 2
    return ret


def getChinese(data, GPy_Table, GTable):
    """
    读取中文表
    """
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len], GPy_Table)

        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 词频
            pos += 2
            count = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 保存
            GTable.append((count, py, word))
            # 到下个词的偏移位置
            pos += ext_len


def scel2txt(file_name):
    """
    转换scel为txt
    """

    # 全局拼音表
    GPy_Table = {}

    # 解析结果
    # 元组(词频,拼音,中文词组)的列表
    GTable = []

    print('-' * 60)
    with open(file_name, 'rb') as f:
        data = f.read()

    print("词库名：", byte2str(data[0x130:0x338]))  # .encode('GB18030')
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))

    getPyTable(data[startPy:startChinese], GPy_Table)

    getChinese(data[startChinese:], GPy_Table, GTable)
    return GTable


def single_file():
    input_path = r'f:\Users\QQT\Documents\Temp\scel1\167\安徽\安徽.scel'  # 输入scel所在文件夹路径
    output_path = r'f:\Users\QQT\Documents\Temp\txt1\167\安徽\安徽.txt'  # 输出txt所在文件夹路径
    # 转换scel为txt
    GTable = scel2txt(input_path)
    # 保存结果
    with open(output_path, 'w', encoding='utf8') as f:
        f.writelines([py + " " + word + '\n' for count, py, word in GTable])


def batch_file(input_dir, output_dir):
    # 创建保存路径
    try:
        os.mkdir(output_dir)
    except Exception as e:
        print(e)
    # 遍历文件夹下的文件
    for parent, dirnames, filenames in os.walk(input_dir):
        new_parent = output_dir + parent.replace(input_dir, "")
        try:
            os.mkdir(new_parent)
        except Exception as e:
            print(e)
        # 批量处理文件
        for filename in filenames:
            if os.path.exists(os.path.join(new_parent, filename.replace('.scel', '.txt'))):
                print(filename + ">>>>>>文件已存在")
            else:
                try:
                    GTable = scel2txt(os.path.join(parent, filename))
                    with open(os.path.join(new_parent, filename.replace('.scel', '.txt')), 'w', encoding='utf8') as f:
                        f.writelines([py + " " + word + '\n' for count, py, word in GTable])  # 此处可选择输出的是词频、拼音或是文字
                        print(filename + ">>>>>>txt转换成功")
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    single_file()  # 单个文件转换

    # Scel保存路径
    # SavePath = r"f:\Users\QQT\Documents\zTemp Files\scel1"
    # TXT保存路径
    # txtSavePath = r"f:\Users\QQT\Documents\zTemp Files\txt1"
    # batch_file(SavePath, txtSavePath)  # 多个文件转换
