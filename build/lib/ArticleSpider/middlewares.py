# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from fake_useragent import UserAgent
from ArticleSpider.utils.crawl_xici_ip import GetIP


class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    # 随机更换User-Agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent_list = crawler.settings.get("user_agent_list", [])
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # from ArticleSpider.settings import user_agent_list
        # import random
        # request.headers.setdefault("User-Agent", user_agent_list[random.randint(0, len(user_agent_list)-1)])

        def get_ua():
            return getattr(self.ua, self.ua_type)

        # random_agent = get_ua()  # 调试的时候用

        request.headers.setdefault("User-Agent", get_ua())
        # request.meta["proxy"] = "http://113.128.90.192:48888"


class RandomProxyMiddleware(object):
    # 动态设置ip代理
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()

from selenium import webdriver
from scrapy.http import HtmlResponse


class JSPageMiddleware(object):
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="G:/Document/PythonServerEnvironment/SelniumWebdriver/chromedriver.exe")
    #     super(JSPageMiddleware, self).__init__()

    # 通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "jobbole":
            # chrome_opt = webdriver.ChromeOptions()
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # chrome_opt.add_experimental_option("prefs", prefs)
            # browser = webdriver.Chrome( executable_path="G:/Document/PythonServerEnvironment/SelniumWebdriver/chromedriver.exe", chrome_options=chrome_opt)
            # browser = webdriver.Chrome(executable_path="G:/Document/PythonServerEnvironment/SelniumWebdriver/chromedriver.exe")
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问：{0}".format(request.url))

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)



