#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/9/10
# @Author  : 圈圈烃
# @File    : Sougou_Spider
# @Description: 搜狗词库爬虫
#
#
from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


class SougouSpider:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    res = ''

    def __init__(self, url):
        self.url = url

    def get_html(self, open_proxy=False, ip_proxies=None):
        try:
            pattern = re.compile(r'//(.*?)/')
            host_url = pattern.findall(self.url)[0]
            SougouSpider.headers["Host"] = host_url
            if open_proxy:  # 判断是否开启代理
                proxies = {"http": "http://" + ip_proxies, }  # 设置代理，例如{"http": "http://103.109.58.242:8080", }
                SougouSpider.res = requests.get(self.url, headers=SougouSpider.headers, proxies=proxies, timeout=5)
            else:
                SougouSpider.res = requests.get(self.url, headers=SougouSpider.headers, timeout=5)
            SougouSpider.res.encoding = SougouSpider.res.apparent_encoding  # 自动确定html编码
            print("Html页面获取成功 " + self.url)
            return SougouSpider.res      # 只返回页面的源码
        except Exception as e:
            print("Html页面获取失败 " + self.url)
            print(e)

    def get_cate_1_list(self):
        # 获取大分类链接
        dict_cate_1_urls = []
        soup = BeautifulSoup(SougouSpider.res.text, "html.parser")
        dict_nav = soup.find("div", id="dict_nav_list")
        dict_nav_lists = dict_nav.find_all("a")
        for dict_nav_list in dict_nav_lists:
            dict_nav_url = "https://pinyin.sogou.com" + dict_nav_list['href']
            dict_cate_1_urls.append(dict_nav_url)
        return dict_cate_1_urls

    def get_cate_2_1_list(self):
        # 获取第一种小分类链接
        dict_cate_2_1_dict = {}
        soup = BeautifulSoup(SougouSpider.res.text, "html.parser")
        dict_td_lists = soup.find_all("div", class_="cate_no_child citylistcate no_select")
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            dict_cate_2_1_dict[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        return dict_cate_2_1_dict

    def get_cate_2_2_list(self):
        # 获取第二种小分类链接
        dict_cate_2_2_dict = {}
        soup = BeautifulSoup(SougouSpider.res.text, "html.parser")
        dict_td_lists = soup.find_all("div", class_="cate_no_child no_select")
        # 类型1解析
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            dict_cate_2_2_dict[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        # 类型2解析
        dict_td_lists = soup.find_all("div", class_="cate_has_child no_select")
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            dict_cate_2_2_dict[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        return dict_cate_2_2_dict

    def get_page(self):
        # 页数
        soup = BeautifulSoup(SougouSpider.res.text, "html.parser")
        dict_div_lists = soup.find("div", id="dict_page_list")
        dict_td_lists = dict_div_lists.find_all("a")
        page = dict_td_lists[-2].string
        return int(page)

    def get_download_list(self):
        # 获取当前页面的下载链接
        dict_dl_dict = {}
        pattern = re.compile(r'name=(.*)')
        soup = BeautifulSoup(SougouSpider.res.text, "html.parser")
        dict_dl_lists = soup.find_all("div", class_="dict_dl_btn")
        for dict_dl_list in dict_dl_lists:
            dict_dl_url = dict_dl_list.a['href']
            dict_name = pattern.findall(dict_dl_url)[0]
            dict_ch_name = unquote(dict_name, 'utf-8').replace("/", "-").replace(",", "-").replace("|", "-")\
                .replace("\\", "-").replace("'", "-")
            dict_dl_dict[dict_ch_name] = dict_dl_url
        return dict_dl_dict

    def download_dict(self, dl_url, path):
        # 下载
        pattern = re.compile(r'//(.*?)/')
        host_url = pattern.findall(dl_url)[0]
        SougouSpider.headers["Host"] = host_url
        proxies = {"http": "http://117.127.0.196:80", }  # 设置代理，例如{"http": "http://103.109.58.242:8080", }
        res = requests.get(dl_url, headers=SougouSpider.headers, proxies=proxies, timeout=5)
        with open(path, "wb") as fw:
            fw.write(res.content)


def main():
    url = "https://pinyin.sogou.com/dict/cate/index/436"
    save_dir = "scel/"
    dirnames = ['城市信息', '自然科学', '社会科学', '工程应用', '农林渔畜', '医学医药',
                '电子游戏', '艺术设计', '生活百科', '运动休闲', '人文科学', '娱乐休闲']
    for dirname in dirnames:
        try:
            os.mkdir(save_dir + dirname)
        except Exception as e:
            print(e)
    # 获取大类链接
    mysougou = SougouSpider(url)
    mysougou.get_html()
    dict_cate_1_urls = mysougou.get_cate_1_list()
    count = 0
    # 大类分类
    for dict_cate_1_url in dict_cate_1_urls:
        # 创建保存路径
        save_dir_1 = save_dir + dirnames[count]  # 大类文件保存路径
        count += 1
        # 获取小类链接
        mysougou.url = dict_cate_1_url
        mysougou.get_html()
        if dict_cate_1_url == "https://pinyin.sogou.com/dict/cate/index/167":
            dict_cate_2_dict = mysougou.get_cate_2_1_list()
        else:
            dict_cate_2_dict = mysougou.get_cate_2_2_list()
        # 小类分类
        for key in dict_cate_2_dict:
            # 创建保存路径
            save_dir_2 = save_dir_1 + "/" + key     # 小类文件保存路径
            try:
                os.mkdir(save_dir_2)
            except Exception as e:
                print(e)
            print(save_dir_2)
            try:
                mysougou.url = dict_cate_2_dict[key]
                mysougou.get_html()
                pages = mysougou.get_page()
            except Exception as e:
                print(e)
                pages = 1
            # 获取下载链接
            for page in range(1, pages + 1):
                page_url = dict_cate_2_dict[key] + "/default/" + str(page)
                mysougou.url = page_url
                mysougou.get_html()
                dict_dl_dict = mysougou.get_download_list()
                # 下载咯
                for name in dict_dl_dict:
                    save_path = save_dir_2 + "/" + name + ".scel"
                    if os.path.exists(save_path):
                        print(name + ">>>>>>文件已存在")
                    else:
                        dl_url = dict_dl_dict[name]
                        mysougou.download_dict(dl_url, save_path)
                        print(name + ">>>>>>保存成功")


if __name__ == '__main__':
    main()
