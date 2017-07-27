#!/usr/bin/python
# coding = utf-8

import base64
import json
from urllib import request
from bs4 import BeautifulSoup
import util
import mongo


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


#抓取文章数据
def catch_data(cmsid,num = 30,cp = 1,priority = 0):
    url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s="+str(num)+"&cp="+str(cp)+"&priority="+str(priority)
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


# 抓取整个类目下的文章
def catch_data_cms(cmsid):
    cp = 0
    while True:
        cp += 1
        data = catch_data(cmsid, 30, cp)
        if data["result"]:
            print('catch article: ', data['result'])
        else:
            print(cmsid, "抓取完成,数量：", data['totalNumber'])
            break

