from pymongo import MongoClient
import time
client = MongoClient("localhost",27017)
db = client.spider
collection = db.cmsid
try:
    re = collection.insert({"_id":"123456", "url":"http://baidu.com","totol":"5000","cp":"1", "status":"0"})
except Exception as e:
    print(e)
print(re)
for col in collection.find({"cmsid":"123456"}):
    print(col)