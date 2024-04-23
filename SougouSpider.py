#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/11/1
# @Author  : 圈圈烃
# @File    : SougouSpider
# @Description:
#
#
from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


class SougouSpider:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def GetHtml(self, url, isOpenProxy=False, myProxies=None):
        """
        获取Html页面
        :param isOpenProxy: 是否打开代理，默认否
        :param Proxies: 代理ip和端口，例如：103.109.58.242:8080，默认无
        :return:
        """
        try:
            pattern = re.compile(r'//(.*?)/')
            hostUrl = pattern.findall(url)[0]
            self.headers["Host"] = hostUrl
            if isOpenProxy:
                proxies = {"http": "http://" + myProxies, }
                resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=5)
            else:
                resp = requests.get(url, headers=self.headers, timeout=5)
            resp.encoding = resp.apparent_encoding
            print("GetHtml成功..." + url)
            return resp
        except Exception as e:
            print("GetHtml失败..." + url)
            print(e)

    def GetCategoryOne(self, resp):
        """获取大类链接"""
        categoryOneUrls = []
        soup = BeautifulSoup(resp.text, "html.parser")
        dict_nav = soup.find("div", id="dict_nav_list")
        dict_nav_lists = dict_nav.find_all("a")
        for dict_nav_list in dict_nav_lists:
            dict_nav_url = "https://pinyin.sogou.com" + dict_nav_list['href']
            categoryOneUrls.append(dict_nav_url)
        return categoryOneUrls

    def GetCategory2Type1(self, resp):
        """获取第一种类型的小类链接"""
        category2Type1Urls = {}
        soup = BeautifulSoup(resp.text, "html.parser")
        dict_td_lists = soup.find_all("div", class_="cate_no_child citylistcate no_select")
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            category2Type1Urls[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        return category2Type1Urls

    def GetCategory2Type2(self, resp):
        """获取第二种类型的小类链接"""
        category2Type2Urls = {}
        soup = BeautifulSoup(resp.text, "html.parser")
        dict_td_lists = soup.find_all("div", class_="cate_no_child no_select")
        # 类型1解析
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            category2Type2Urls[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        # 类型2解析
        dict_td_lists = soup.find_all("div", class_="cate_has_child no_select")
        for dict_td_list in dict_td_lists:
            dict_td_url = "https://pinyin.sogou.com" + dict_td_list.a['href']
            category2Type2Urls[dict_td_list.get_text().replace("\n", "")] = dict_td_url
        return category2Type2Urls

    def GetPage(self, resp):
        """获取页码"""
        soup = BeautifulSoup(resp.text, "html.parser")
        dict_div_lists = soup.find("div", id="dict_page_list")
        dict_td_lists = dict_div_lists.find_all("a")
        page = dict_td_lists[-2].string
        return int(page)

    def GetDownloadList(self, resp):
        """获取下载链接"""
        downloadUrls = {}
        pattern = re.compile(r'name=(.*)')
        soup = BeautifulSoup(resp.text, "html.parser")
        dict_dl_lists = soup.find_all("div", class_="dict_dl_btn")
        for dict_dl_list in dict_dl_lists:
            dict_dl_url = dict_dl_list.a['href']
            dict_name = pattern.findall(dict_dl_url)[0]
            dict_ch_name = unquote(dict_name, 'utf-8').replace("/", "-").replace(",", "-").replace("|", "-") \
                .replace("\\", "-").replace("'", "-")
            downloadUrls[dict_ch_name] = dict_dl_url
        return downloadUrls

    def Download(self, downloadUrl, path, isOpenProxy=False, myProxies=None):
        """下载"""
        pattern = re.compile(r'//(.*?)/')
        hostUrl = pattern.findall(downloadUrl)[0]
        self.headers["Host"] = hostUrl
        if isOpenProxy:
            proxies = {"http": "http://" + myProxies, }
            resp = requests.get(downloadUrl, headers=self.headers, proxies=proxies, timeout=5)
        else:
            resp = requests.get(downloadUrl, headers=self.headers, timeout=5)
        with open(path, "wb") as fw:
            fw.write(resp.content)
