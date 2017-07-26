#!python
#coding = utf-8

import base64
import re
import json
from urllib import request
from pymongo import MongoClient
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
client = MongoClient("localhost", 27017)
db = client.spider
count = 1

def getlist(url):
    pass

# 抓取单个cmsid
def catch_cmsid(url):
    try:
        req = request.Request(url, None, headers)
        html = request.urlopen(req).read()
        html = html.decode('gbk')
        p = 'hxPage.cmsID="(.*?)";'
        cmsid =  re.findall(p, html)[0]
        # if cmsid:
        return cmsid
    except Exception as e:
        print(str(e))

# 抓取全部cmsid
def catch_cmsid_all():
    try:
        #抓取板块信息
        url = "http://www.hexun.com/"
        nav = [] #导航列表[{name,url,status}]
        cmsid_link = []

        req = request.Request(url, None, headers)
        html = request.urlopen(req).read()
        try:
            html = html.decode("gbk")
        except Exception as e:
            html = html.decode("utf-8")
        dom = BeautifulSoup(html,"html5lib")
        for a in dom.select(".newsTop a"):
            nav.append({"name": a.string,"url": a['href']})
        print("抓取板块分类", len(nav))

        for item in nav:

            threads = []
            for i in range(threadNum):
                t = threading.Thread(target=download_tie)
                threads.append(t)
            for i in range(threadNum):
                threads[i].start()
            for i in range(threadNum):
                threads[i].join()

            count+=1
            print("分析板块内容：",item['name'],item['url'])
            req = request.Request(item["url"],None,headers)
            try:
                html = request.urlopen(req).read()
            except Exception as e:
                continue
            try:
                html = html.decode("gbk")
            except Exception as e:
                html = html.decode("utf-8")
            dom = BeautifulSoup(html, "html5lib")
            for a in dom.select("a"):
                # 过滤url
                if not a.string:
                    print(a)
                    continue
                try:
                    if not "http" in a['href']:
                        continue
                    if a['href'].count("/")>4:
                       continue
                    if not "hexun.com" in a['href']:
                        print("外链\n")
                except Exception as e:
                    continue

                print("分析二级链接的内容:", a['href'])
                count+=1
                req = request.Request(a['href'],None,headers)
                try:
                    html = request.urlopen(req).read()
                except Exception as e:
                    continue
                try:
                    html = html.decode("gbk")
                except Exception as e:
                    try:
                        html = html.decode("utf-8")
                    except Exception as e:
                        pass

                dom = BeautifulSoup(html, "html5lib")
                for a in dom.select("a"):
                    if a.string and ("更多" == a.string):
                        cmsid_link.append(a)
    except Exception as e:
        print(str(e))
    print(cmsid_link)
    print("爬取的总页数：",count)


# 从mongodb中获取cmsID
def get_cmsid(num):
    collection = db.cmsid
    res = collection.find({"status":"0"}).limit(num)
    cmsids = []
    for cmsid in res:
        cmsids.append(cmsid)
    return cmsids

#抓取文章数据
def catch_data(cmsid,num = 30,cp = 1,priority = 0):
    url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s="+str(num)+"&cp="+str(cp)+"&priority="+str(priority)
    try:
        req = request.Request(url,None,headers)
        data = request.urlopen(req).read()
        data = data.decode('gbk')
        # 去除回调函数
        # data = data.split("( ")[1]
        # data = data.split(" )")[0]
        data = json.loads(data)
        for result in data['result']:
            result['content'] = base64.b64decode(result['content'])
            result['content'] = result['content'].decode('gbk')
            # 拼装日期
            result['entitytime'] = result['entityurl'].split('/')[3] +" "+ result['entitytime'].split(' ')[1]
        return data
    # content，title，id，entitytime，entityurl，cms{cmsid,cmstitle}
    except Exception as e:
        print(str(e))

# 抓取整个类目下的文章
def catch_data_all(cmsid):
    cp = 0
    while True:
        cp += 1
        data = catch_data(cmsid, 30, cp)
        if data["result"]:
            print('catch article: ', data['result'])
        else:
            print(cmsid, "抓取完成,数量：", data['totalNumber'])
            break

def run():
    catch_cmsid_all()
    # print(get_cmsid(2))


run()
# path = "status.txt"
# file = open(path, 'w')
# file.write("fasd\n")
# file.close()
