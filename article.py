#!/usr/bin/python
# coding = utf-8

import base64
import json
from urllib import request
import mongo
import util

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


# 单次抓取文章数据
def catch_data(cmsid, step=200, page=1, priority=0):
    if int(step) > 200:
        print("max 200", step)
    url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s="+str(step)+"&cp="+str(page)+"&priority="+str(priority)
    try:
        req = request.Request(url, None, headers)
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
        print("catch_data",str(e))


# 抓取某个类目下的文章
def catch_data_cms(cmsid):
    total = cmsid['total']
    step = 200  # 每次抓取文章的数量
    current = 1

    if not cmsid:
        return
    while True:
        tail = total % current  # 余数
        page = total // step
        page = page if tail else page+1
        data = catch_data(cmsid['cmsid'], step=step, page=page)
        if data:
            util.view_bar(current, total)
            print(current, "/", total, end='')
            num = len(data['result'])
            mongo.set_page_cmsid(cmsid['_id'], num)
            current = current + num

            if current >= total:
                print(cmsid, "抓取完成,数量：", cmsid['current'])
                break
            # for article in data["result"]:
                # print('catch article: ', print(article['id']))


# 抓取整站文章
def catch_article_all():

    cmsid = mongo.get_cmsid(cmsid="101077663")
    print(cmsid)
    catch_data_cms(cmsid)

    # while True:
    #     cmsids = mongo.get_cmsid()
    #     cmsids = cmsids[0]


catch_article_all()
