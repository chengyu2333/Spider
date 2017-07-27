#!/usr/bin/python
# coding = utf-8

from pymongo import MongoClient
import time

client = MongoClient("localhost", 27017)
db = client.spider


# 添加cmsID到mongodb
def add_cmsid(cmsid,cmstitle,cmsurl,group):
    collection = db.cmsid
    return collection.insert({"_id":cmsurl,"cmsid":cmsid,"cmstitle":cmstitle,"group":group,"cp":"1"})


# 从mongodb中获取cmsID
def get_cmsid(num,api = True):
    collection = db.cmsid
    res = collection.find({"status":"0"}).limit(num)
    cmsids = []
    for cmsid in res:
        cmsids.append(cmsid)
    return cmsids


# 标记cmsid抓取的数量和总数， 0：抓取完毕
def page_cmsid(url, page ,totol=0):
    collection = db.cmsid
    result = collection.update({"_id":url}, {"$set":{"cp":page,"totol":totol}})
    print(result)


def add_article(article):
    collection = db.article

page_cmsid("http://futures.hexun.com/nyzx/","30",totol="10000")