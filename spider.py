import cmsid
import  article

def run():
    # 抓取所有cmsid
    cmsid.catch_cmsid_all(True)
    # 测试抓取cmsid
    # print(cmsid.catch_cmsid("http://futures.hexun.com/topic/"))

    # 抓取栏目下所有文章
    # article.catch_data_cms("101790787")

    #测试抓取文章
    # data = article.catch_data("101790787")
    # print(data)

run()