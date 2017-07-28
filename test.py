from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.spider
coll = db.article
# re = coll.find({"_id":101225916})
# print(re[0])


import threading
import time

COUNT = 10


def printHello():
    global COUNT
    print(COUNT)
    COUNT = COUNT - 1


printHello()