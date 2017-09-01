# -*- coding: utf-8 -*-
import re
import scrapy
import json
import datetime
try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
from ArticleSpider.settings import user_agent_list



class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # question的第一页answer得请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/26234383/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"


    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": agent,

    }
    custom_settings = {
        "COOKIES_ENABLED" : True
    }

    def parse(self, response):
        # 提取出html页面中的所有url 并跟踪url进行一些爬取
        # 如果提取得url中格式为 /question/xxx 就下载进行之后直接进入解析函数
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到得question相关页面则下载交由提取函数进行提取
                request_url = match_obj.group(1)
                # 简单的随机更换User-Agent
                # import random
                # random_index = random.randint(0, len(user_agent_list) - 1)
                # random_agent = user_agent_list[random_index]
                # self.headers["User-Agent"] = random_agent
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
                # break  # debug时候用
            else:
                # 如果不是question 页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)  # debug 注释

    def parse_question(self, response):
        # 处理question页面， 从页面中提取question 具体item
        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))

        if "QuestionHeader-title" in response.text:
            # 处理新版本
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("topics", ".QuestionHeader-topics.Popover::text")

        else:
            # 处理知乎旧版本
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
            item_loader.add_css("topics", ".QuestionHeader-topics.Popover::text")

        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item  # debug 注释

    def parse_answer(self, response):
        # 处理answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        # totals_answer = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    def login(self, response):

        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response_text, re.DOTALL)
        if match_obj:
            print(match_obj.group(1))
            _xsrf = match_obj.group(1)
        if _xsrf:

            post_data = {
                "_xsrf": _xsrf,
                "phone_num": '13342266862',
                "password": '553768563',
                "captcha": "",

            }
            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha)   # 重点

    def login_after_captcha(self, response):
        with open("captcha.gif", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open("captcha.gif")
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器的返回数据是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

