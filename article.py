#!/usr/bin/python
# coding = utf-8
import base64
import json
from urllib import request
import mongo
import util
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


# 单次抓取文章数据
def catch_article(cmsid, step=200, page=1, priority=0):
    if int(step) > 200:
        print("max 200", step)
    url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s="+str(step)+"&cp="+str(page)+"&priority="+str(priority)
    # print(url)
    try:
        req = request.Request(url, None, headers)
        data = request.urlopen(req).read()
        data = data.decode('gbk', errors="ignore")
        # 去除回调函数
        # data = data.split("( ")[1]
        # data = data.split(" )")[0]
        data = json.loads(data)
        for result in data['result']:
            result['content'] = base64.b64decode(result['content'])
            result['content'] = result['content'].decode('gbk', errors="ignore")
            # 拼装日期
            result['entitytime'] = result['entityurl'].split('/')[3] +" "+ result['entitytime'].split(' ')[1]
        return data
    except Exception as e:
        print("x", end='')


# 抓取某个类目下的文章
def catch_article_cms(cmsid):
    if not cmsid:
        return
    print("开始抓取【", str(cmsid['cmstitle']), "】")
    total = cmsid['total']
    step = 200  # 每次抓取文章的数量
    current = cmsid['current']
    tail = total % current  # 余数
    max_page = total//step
    max_page = max_page if tail else max_page + 1
    page = current//step
    while True:
        page += 1
        if page >= max_page:
            print("\n【%s  %d】抓取完成,总数量:%d  重"
                  "复数量:%d" % (cmsid['cmstitle'], cmsid['cmsid'], cmsid['total'], mongo.duplicate_key))
            break
        data = catch_article(cmsid['cmsid'], step=step, page=page)
        if data:
            util.view_bar(current, total)
            print(current, "/", total, end='')
            num = len(data['result'])
            mongo.set_page_cmsid(cmsid['_id'], num)
            current = current + num
            mongo.add_article(data, cmsid)  # 存入数据库
            # if current >= total:
            #     print("\n【%s  %d】抓取完成,总数量数量:%d 重"
            #           "复数量:%d" % (cmsid['cmstitle'], cmsid['cmsid'], cmsid['total'], mongo.duplicate_key))
            #     break


# 抓取整站文章
def catch_article_all():
    cmsids = mongo.get_cmsid(999)
    print("还有%d个板块待抓取" % len(cmsids))
    for cmsid in cmsids:
        catch_article_cms(cmsid)

