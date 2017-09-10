#!/usr/bin/env python
# -*- coding:utf-8 -*-

__Author__ = "HackFun"

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalysis

from elasticsearch_dsl.connections import connections

es = connections.create_connection(hosts=["localhost"])  # connection可以连接多台服务器


class CustomAnalyzer(_CustomAnalysis):
    def get_analysis_definition(self):
        return {}

ik_analyser = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(DocType):
    # 伯乐在线文章类型
    # suggest = Completion(analyzer="ik_max_word")  # 不能直接使用这个，由于源码问题，必须使用CustomAnalyzer
    suggest = Completion(analyzer=ik_analyser)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = "article"


if __name__ == "__main__":
    ArticleType.init()  # 根据类，直接生成mapping，
