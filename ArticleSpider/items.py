# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
from w3lib.html import remove_tags
from ArticleSpider.models.es_types import ArticleType
import redis


from elasticsearch_dsl.connections import connections

es = connections.create_connection(ArticleType._doc_type.using)

redis_cli = redis.StrictRedis()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now()
    return create_date


def add_jobbole(value):
    return value+"-haifeng"


def get_nums(value):
    # print(value)
    match_re = re.match(r'.*?(\d+).*', value)
    if match_re:
        nums = match_re.group(1)
        return nums
    else:
        return 0


def remove_comment_tags(value):
    # 去掉tag中提取得评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数据
    # python工程师  title  10
    # python工程师  text   3
    # 不能覆盖，所以用set
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es得analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            analyzed_words = set(r["token"] for r in words["tokens"] if len(r["token"]) > 1)
            new_words = analyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests


class ArticleItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # title = scrapy.Field(
    #     input_processor=MapCompose(lambda x: x+"-jobbole", add_jobbole),
    #     output_processor = TakeFirst()
    # )
    title = scrapy.Field()

    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(","),
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into jobbole(title, url, create_date, fav_nums)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY 
                            UPDATE title=VALUES(title),url=VALUES(url),
                            create_date=VALUES (create_date),fav_nums=VALUES (fav_nums) 
                            """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"])
        return insert_sql, params

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]

        # article.suggest = [{"input":[], "weight":2}]
        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))

        article.save()

        redis_cli.incr("jobble_count")

        return


class ZhihuQuestionItem(scrapy.Item):
    # 知乎的问题 Item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, 
                            watch_user_num, click_num, crawl_time)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)
                            ON DUPLICATE KEY 
                            UPDATE content=VALUES(content),answer_num=VALUES(answer_num), 
                            comments_num=VALUES (comments_num),watch_user_num=VALUES (watch_user_num), 
                            click_num=VALUES (click_num)  
                            """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        watch_user_num = extract_num("".join(self["watch_user_num"]))
        click_num = extract_num("".join(self["click_num"]))
        crawl_time = datetime.datetime.now().strftime("")

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
                            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, 
                            comments_num,create_time, update_time, crawl_time) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s) 
                            ON DUPLICATE KEY 
                            UPDATE content=VALUES(content),comments_num=VALUES(comments_num),
                            praise_num=VALUES (praise_num),update_time=VALUES (update_time) 
                            """  # on duplicate是mysql特有的语法
        create_time = datetime.datetime.fromtimestamp(self["create_time"])
        update_time = datetime.datetime.fromtimestamp(self["update_time"])

        params = (
            self["zhuhu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time, self["crawl_time"],
        )


def remove_splash(value):
    # 去掉工作城市得斜线
    return value.replace("/", "")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_out_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉钩网职位信息
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(Join(","))
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags),
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into 
            lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need, job_type,publish_time,
            tags, job_advantage, job_desc, job_addr, company_url, company_name, crawl_time, crawl_update_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            salary=VALUES (salary), job_desc=VALUES (job_desc), crawl_update_time=VALUES (crawl_update_time)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"], self["work_years"],
            self["degree_need"],self["job_type"], self["publish_time"], self["tags"], self["job_advantage"],
            self["job_desc"],self["job_addr"], self["company_url"], self["company_name"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT), self["crawl_update_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params




