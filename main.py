#!/usr/bin/python
# encoding: utf-8

from bs4 import BeautifulSoup
import urllib
import util
from urllib import request
import re
import threading
import sys
import time
import pymongo

url_index = "http://www.hexun.com/"
url_article = "http://funds.hexun.com/2017-07-25/190175893.html"

# 规则配置说明
# name：名称，url：待抓取网址，rule_title（有规律的url：http://test.com/menu-$[page].html）：标题匹配规则，rule_page_url：翻页url匹配规则
# rule_page_max：最大页码匹配规则（如果是有规律的网址）
# js_enable：是否需要启用js引擎
rules_url = [{'name': '新三板', 'column_url': 'http://news.hexun.com/company/', 'article_title': '.mainboxcontent li a', 'rule_page_url': '#page2011nav'},]

config = {'max_thread': 100,
          'sleep': 0,
          'max_url_cache': 100
          }
url_cache = []
headers = {"User-Agent": util.config_get('spider', 'user_agent')}


# 一次抓取单个章内容
def catch_article_single(url):
    try:
        id = url.split("/")[4].split(".")[0]
        req = request.Request(url, headers=headers)
        html = request.urlopen(req).read()
        dom_html = BeautifulSoup(html, "html5lib")
        title = dom_html.select(".articleName > h1")[0].string
        time = dom_html.select(".pr20")[0].string
        original = dom_html.select(".pr20 + a")[0]
        original = str(original)
        content = dom_html.select(".art_contextBox")[0]
        author = dom_html.select(".art_contextBox div[style='text-align:right;font-size:12px']")[0].text
        return {"id":id,"entityurl": url, "title": title, "entitytime": time, "original": original, "author": author, "content": content}
    except Exception as e:
        print(str(e))
    finally:
        pass


# 获取栏目信息
def catch_column():
    pass


# 获取文章地址
def catch_url():
    for rule in rules_url:
        try:
            print('rule:', rule)
            req = request.Request(rule['column_url'], None, headers)
            html = request.urlopen(req).read()
            html = util.html_decode(html)
            dom = BeautifulSoup(html, "html5lib")
            dom_title = dom.select(rule['article_title'])
            print("title-list:", dom_title)

            # for title in dom_title:
            #     print("title:", title.string, "   ", title['href'])
        except Exception as e:
            print(str(e))


# 开始运行
def run():
    pass
    # print(catch_article(url_article))
    catch_url()
    url1 = "http://forex.hexun.com/2017-07-24/190162151.html"
    # data = catch_article_single(url1)
    # print(data['title'])

run()