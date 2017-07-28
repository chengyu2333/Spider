#!/usr/bin/python
# coding = utf-8

from pymongo import MongoClient
from pymongo import errors
import time

client = MongoClient("localhost", 27017)
db = client.spider

duplicate_key = 0

# 添加新的cmsID到mongodb
def add_cmsid(cmsid,cmstitle,cmsurl,group,total):
    collection = db.cmsid
    return collection.insert({"_id":cmsurl,"cmsid":int(cmsid),"cmstitle":cmstitle,"group":group,"current":1,"total":int(total)})


# 从mongodb中获取cmsID
def get_cmsid(num=1, api=True,cmsid="0"):
    collection = db.cmsid
    if int(cmsid):
       return collection.find_one({"cmsid": int(cmsid)})
    if api:
        res = collection.find({"$where": "this.cmsid>0 && this.total>this.current"}).limit(num)
    else:
        res = collection.find({"$where": "this.cmsid==0 && this.total==0"}).limit(num)
    cmsids = []
    for cmsid in res:
        cmsids.append(cmsid)
    return cmsids


# 增加抓取的数量
def set_page_cmsid(url, num):
    collection = db.cmsid
    result = collection.update({"_id": url}, {"$inc": {"current":num}})
    return result


# 获取cmsid文章数量
def get_total(url):
    collection = db.cmsid
    result = collection.find({"_id": url})
    print(result['total'])


# 添加文章
def add_article(data,cms):
    global duplicate_key
    collection = db.article
    for article in data['result']:
        article['_id'] = article['id']
        del article['id']
        article['cmsid'] = cms
        try:
            collection.insert(article)
        except errors.DuplicateKeyError as dk:
            duplicate_key = duplicate_key + 1
        except Exception as e:
            print(str(e))


# 恢复抓取状态
def recover_status():
    collection = db.cmsid
    re = collection.update({"current": {"$gt": 1}}, {"$set": {"current": 1}},multi=True)
