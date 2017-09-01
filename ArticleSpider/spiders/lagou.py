# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItem, LagouJobItemLoader
from ArticleSpider.utils.common import get_md5
import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", "")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text")
        item_loader.add_css("work_years", ".job_request p span:nth-child(3)::text")  # 这里使用css ，是为了在学习时，熟悉css选择器用法
        item_loader.add_xpath("degree_need", "//dd[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//dd[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("tags", ".position-label.clearfix li::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_value("crawl_time", datetime.datetime.now())
        # item_loader.add_css("crawl_update_time", datetime.datetime.now())

        job_item = item_loader.load_item()  # 这里先赋值给一个变量，是考虑到便于调试以及代码可读性，而不是为了代码简洁而直接return

        return job_item

    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results