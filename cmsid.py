#!/usr/bin/python
# encoding: utf-8

import re
import threading
import json
from urllib import request
from pymongo import errors
from bs4 import BeautifulSoup
import util
import mongo
headers = {"User-Agent": util.config_get('spider', 'user_agent')}


# 抓取栏目文章总数
def catch_total(cmsid):
    if int(cmsid):
        url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s=1&cp=1&priority=0"
        req = request.Request(url,None,headers)
        data = request.urlopen(req).read().decode("gbk", errors="ignore")
        data = json.loads(data)
        return data['totalNumber']
    else:
        return 0


# 抓取单个cms信息
def catch_cmsid(url):
    try:
        if not util.url_filter(url):
            return

        req = request.Request(url, None, headers)
        html = request.urlopen(req).read()
        html = util.html_decode(html)
        dom = BeautifulSoup(html, "html5lib")

        if dom.select("title"):
            title = dom.select("title")[0].string

        # 匹配是否为cms页和类型
        if 'hxPage.cmsID' in html: # 有api
            cmsid = re.findall('hxPage.cmsID="(\d+?)";', html)[0]
            return {"cmsid": cmsid, "cmstitle": title, "cmsurl": url, "total": catch_total(cmsid)}
        elif 'hxPage.maxPage' in html:
            cmsid = "0"
            total = re.findall('hxPage.maxPage(\d+?);', html)[0]
        elif 'hxPage.numPage' in html:  # 无api
            cmsid = "0"
            total = re.findall('hxPage.numPage=(\d+?);', html)[0]
        else:
            return None
        return {"cmsid":cmsid, "cmstitle":title, "cmsurl":url, "total": total}
    except Exception as e:
        print("x ", end='')


# 分析二级链接含有cms
def analyse(item):
    if not util.url_filter(item["url"]):
        return

    print("分析板块内容：", item['name'], item['url'])
    req = request.Request(item["url"], None, headers)
    try:
        html = request.urlopen(req).read()
    except Exception as e:
        print("catch nav", str(e))
    html = util.html_decode(html)
    dom = BeautifulSoup(html, "html5lib")

    for a in dom.select("a"):
        # 过滤url,不符合直接跳过
        if not a.string:
            continue
        try:
            if not util.url_filter(a['href']):
                continue
        except Exception as e:
            continue

        # print("分析二级链接的内容:", a['href'])
        print(". ", end='')
        req = request.Request(a['href'], None, headers)
        try:
            html = request.urlopen(req).read()
        except Exception as e:
            continue
        html = util.html_decode(html)
        if html:
            dom = BeautifulSoup(html, "html5lib")
        else:
            continue
        for a in dom.select("a"):
            # 匹配特征
            if a.string and ("更多" == a.string):
                print("o ", end='')
                # 尝试抓取cmsid
                cmsid = catch_cmsid(a['href'])
                if cmsid:
                    try:
                        # 存入mongoDb
                        mongo.add_cmsid(cmsid['cmsid'], cmsid['cmstitle'], cmsid['cmsurl'], item['name'], cmsid['total'])
                        print("√ ", end='')
                    except errors.DuplicateKeyError as dk:
                        print("E ", end='')
                    except Exception as e:
                        print("X ", end='')


# 抓取全部cmsid
def catch_cmsid_all(thread=False, start=1, end=0):
    current = 0
    try:
        # 抓取板块信息
        url = "http://www.hexun.com/"
        nav = []  # 导航列表[{name,url}]

        req = request.Request(url, None, headers)
        html = request.urlopen(req).read()
        html = util.html_decode(html)
        dom = BeautifulSoup(html,"html5lib")
        for a in dom.select(".newsTop a"):
            nav.append({"name": a.string, "url": a['href']})
        print("抓取板块数量：", len(nav))

        if not end:
            end = len(nav)

        if thread:
            # 开启线程分析子版块
            threads = []
            for item in nav:
                t = threading.Thread(target=analyse, args=(item,))
                threads.append(t)
            for i in range(len(threads)):
                if start <= i+1 <= end:
                    threads[i].start()
            for i in range(len(threads)):
                if start <= i + 1 <= end:
                    threads[i].join()
        else:
            # 单线程
            for item in nav:
                current += 1
                if start <= current <= end:
                    analyse(item)
    except Exception as e:
        print("catch_cmsid_all", str(e))
