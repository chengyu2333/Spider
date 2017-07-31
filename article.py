#!/usr/bin/python
# encoding: utf-8
from bs4 import BeautifulSoup
import os
import threading
import time
import base64
import json
from urllib import request
import mongo
import util
headers = {"User-Agent": util.config_get('spider', 'user_agent')}
current = 0
total = 0


# 下载图片
def down_pic(url, path):
    try:
        request.urlretrieve(url, path)
    except Exception as e:
        pass


# 获取评论
def catch_comment(article_id):
    url = "http://comment.tool.hexun.com/Comment/GetComment.do?commentsource=1&articlesource=1&articleid="+str(article_id)+"&pagesize=100&pagenum=1"
    try:
        req = request.Request(url, None, headers)
        data = request.urlopen(req).read()
        data = data.decode('gbk', errors="ignore")
        # 去首位括号
        data = data[1:]
        data = data[:-1]
        data = json.loads(data)
        return data['revdata']['articledata']
    except Exception as e:
        print(e)


# 一次抓取多个文章数据
def catch_article_multi(cmsid, step=100, page=1, priority=0):
    global current, total
    threads_img = []
    threads_comment = []
    if int(step) > 200:
        step = 200
    url = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id="+str(cmsid)+"&s="+str(step)+"&cp="+str(page)+"&priority="+str(priority)
    # print(url)
    try:
        req = request.Request(url, None, headers)
        data = request.urlopen(req).read()
        data = data.decode('gbk', errors="ignore")
        data = json.loads(data)
        for result in data['result']:
            util.view_bar(current, total)
            print(current, "/", total, end='\n')
            current += 1
            result['content'] = base64.b64decode(result['content'])
            result['content'] = result['content'].decode('gbk', errors="ignore")
            # 拼装日期
            result['entitytime'] = result['entityurl'].split('/')[3] + " " + result['entitytime'].split(' ')[1]
            # 拼装ID
            # result['id'] = int(result['entityurl'].split('/')[3].replace('-', '')) + result['id']
            # 抓取评论
            result['comment'] = catch_comment(result['id'])
            # 抓取图片
            dom = BeautifulSoup(result['content'], "html5lib")
            dom_img = dom.select('img')
            for img in dom_img:
                # 不存在img则直接跳过
                try:
                    img_url = img['src']
                    suffix = img_url.split(".")[-1]
                    file_name_hash = util.md5(img_url)
                    img_dir_path = file_name_hash[0:3] + "/" + file_name_hash[4:7]
                    img_fullname = img_dir_path + "/" + file_name_hash + "." + suffix
                    if util.isWindowsSystem():
                        img_dir_path = ("E:/spider_data/" + img_dir_path).encode("gbk")
                        img_fullname = ("E:/spider_data/" + img_fullname).encode("gbk")
                    else:
                        img_dir_path = "~/spider_data/" + img_dir_path
                    if not os.path.exists(img_dir_path):
                        os.makedirs(img_dir_path)
                    t = threading.Thread(target=down_pic, args=(img_url, img_fullname.decode()))
                    threads_img.append(t)
                    img['src'] = img_fullname.decode()
                except Exception as e:
                    print(e)
                    continue
            result['content'] = str(dom.body)

        # 多线程下载图片
        # print("thread count:", len(threads))
        for i in threads_img:
            i.start()
        for i in threads_img:
            i.join()

        return data
    except Exception as e:
        print("x"+str(e), end='')
    finally:
        pass


# 抓取某个类目下的文章
def catch_article_cms(cmsid):
    global current, total
    if not cmsid:
        return
    print("开始抓取【", str(cmsid['cmstitle']), "】")
    total = cmsid['total']
    step = int(util.config_get('spider', 'catch_article_num'))  # 每次抓取文章的数量
    current = cmsid['current']
    tail = total % current  # 余数
    max_page = total//step
    max_page = max_page if tail else max_page + 1
    page = current//step
    while True:
        page += 1
        if page >= max_page:
            current = 0
            total = 0
            print("\n【%s  %d】抓取完成,总数量:%d  重"
                  "复数量:%d" % (cmsid['cmstitle'], cmsid['cmsid'], cmsid['total'], mongo.duplicate_key))
            break
        data = catch_article_multi(cmsid['cmsid'], step=step, page=page)
        if data:
            mongo.set_page_cmsid(cmsid['_id'], len(data['result']))
            mongo.add_article(data, cmsid)  # 存入数据库


# 抓取整站文章
def catch_article_all():
    cmsids = mongo.get_cmsid(999)
    print("还有%d个板块待抓取" % len(cmsids))
    for cmsid in cmsids:
        catch_article_cms(cmsid)

