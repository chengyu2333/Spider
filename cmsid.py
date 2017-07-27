#!/usr/bin/python
# coding = utf-8

import re
import threading
import time
from urllib import request
from bs4 import BeautifulSoup
import util
import mongo


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


# 抓取单个cmsid
def catch_cmsid(url):
    try:
        if not util.url_filter(url):
            return

        req = request.Request(url, None, headers)
        try:
            html = request.urlopen(req).read()
            html = util.html_decode(html)
            dom = BeautifulSoup(html, "html5lib")
        except Exception as e:
            print(url,str(e))
            return

        if 'hxPage.cmsID' in html:
            cmsid = re.findall('hxPage.cmsID="(.*?)";', html)[0]
        elif 'hxPage.maxPage' in html or 'hxPage.numPage' in html:
            cmsid = "0"
        else:
            return None
        if dom.select("title"):
            title = dom.select("title")[0].string
        return {"cmsid":cmsid, "cmstitle":title,"cmsurl":url}

    except Exception as e:
        print("catch_cmsid：",str(e))



# 分析二级链接是否含有cmsId
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
        print("· ", end='')
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
                print("√ ", end='')
                # 尝试抓取cmsid
                cmsid = catch_cmsid(a['href'])
                if cmsid:
                    try: # 存入mongoDb
                        mongo.add_cmsid(cmsid['cmsid'], cmsid['cmstitle'], cmsid['cmsurl'], item['name'])
                        print("\n", cmsid)
                    except Exception as e:
                        print("x ", end='')


# 抓取全部cmsid
def catch_cmsid_all():
    try:
        #抓取板块信息
        url = "http://www.hexun.com/"
        nav = [] #导航列表[{name,url,status}]

        req = request.Request(url, None, headers)
        html = request.urlopen(req).read()
        html = util.html_decode(html)
        dom = BeautifulSoup(html,"html5lib")
        for a in dom.select(".newsTop a"):
            nav.append({"name": a.string,"url": a['href']})
        print("抓取板块数量：", len(nav))

        # 开启线程分析子版块
        threads = []
        for item in nav:
            t = threading.Thread(target=analyse, args=(item,))
            threads.append(t)
            break
        print("开启了的线程数",len(threads))
        for i in range(len(nav)):
            threads[i].start()
        for i in range(len(nav)):
            threads[i].join()

    except Exception as e:
        print("catch_cmsid_all", str(e))
