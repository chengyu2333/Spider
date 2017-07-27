#!/usr/bin/python
# coding = utf-8

from pymongo import MongoClient
import time

client = MongoClient("localhost", 27017)
db = client.spider


# 添加新的cmsID到mongodb
def add_cmsid(cmsid,cmstitle,cmsurl,group,total):
    collection = db.cmsid
    return collection.insert({"_id":cmsurl,"cmsid":int(cmsid),"cmstitle":cmstitle,"group":group,"current":1,"total":int(total)})


# 从mongodb中获取cmsID
def get_cmsid(num=1, api=True):
    collection = db.cmsid
    if api:
        res = collection.find({"$where": "this.cmsid>0 && this.total>this.current"}).limit(num)
    else:
        res = collection.find({"$where": "this.cmsid==0 && this.total==0"}).limit(num)
    cmsids = []
    for cmsid in res:
        cmsids.append(str(cmsid))
    return cmsids


# 增加抓取的数量
def set_page_cmsid(url, num):
    collection = db.cmsid
    result = collection.update({"_id": url}, {"$inc": {"current":num}})
    print(result)

# 设置cmsid文章数量
def get_total(url):
    collection = db.cmsid
    result = collection.find({"_id": url})
    print(result['total'])

# 添加文章
def add_article(article):
    collection = db.article
    return collection.insert(article)

# page_cmsid("http://futures.hexun.com/nyzx/","30",totol="10000")
