import cmsid
import time
import article
import mongo

def run():
    # 恢复抓取状态
    mongo.recover_status()

    # 抓取所有cmsid
    cmsid.catch_cmsid_all(thread=False, start=2)

    # 测试抓取单个cmsid
    # print(cmsid.catch_cmsid("http://futures.hexun.com/topic/"))

    # 抓取栏目下所有文章

    # cms = mongo.get_cmsid(cmsid="101077663")
    # article.catch_article_cms(cms)

    # 抓取整站文章
    # article.catch_article_all()

run()

print("任务完成")
time.sleep(600)
