# ArticleSpider
通过scrapy，爬取知乎，伯乐在线，拉钩网

**注：**

> 这是一个进阶项目，需要有一定的爬虫知识，如果不是很懂基本的爬虫原理，请自行学习一下爬虫基础知识。
我有一个对应的仓库[MyPythonForSpider](http://git.oschina.net/hackfun/MyPythonForSpider "baidumusicspider")，是一个单线程爬取百度音乐数据的实例，比较适合刚入门的朋友。



**这是一个基于web抓取框架[scrapy](https://baike.baidu.com/item/scrapy/7914913?fr=aladdin "scrapy")，实现的对于知乎，伯乐在线，拉勾网的爬取。**

### 涉及到的知识点
<pre>
|-- 基础
|   |-- 正则表达式 [jobbole.py](ArticleSpider/spiders/jobbole.py）
|   |-- xpath （ArticleSpider/spiders/jobbole.py）
|   |-- css选择器 （ArticleSpider/spiders/*.py）
|   `-- ItemLoader
|-- 进阶
|   |-- 图片验证码的处理（ArticleSpider/spiders/lagou.login_after_captcha）
|   |-- ip访问频率限制（ArticleSpider.middlewares.RandomProxyMiddleware）
|   `-- user-agent随机切换（ArticleSpider.middlewares.RandomUserAgentMiddleware）
|-- 高级
|   |-- scrapy的原理
|       `-- 基于scrapy的中间件开发
|   |-- 动态网站的抓取处理
|   |-- 将selenium集成到scrapy中 
|   `-- scrapy log配置
`-- |后续(在此项目中没有体现，后续我将上传此部分代码)
    |-- scrapy-redis
        |-- 分布式爬虫原理
        |-- 分析scrapy-redis源码
        `-- 集成bloomfilter到scrapy-redis中
    `-- Elasticsearch （ArticleSpider.pipelines.ElasticsearchPipeline;）(ArticleSpider.items.JobBoleArticleItem.save_to_es;)
        |-- 安装 elasticsearch-rtf
        |-- 学习使用 elasticsearch-head、kibana
        |-- 学习使用 elasticsearch的Python API： elasticsearch-dsl
        `-- 利用elasticsearch和爬取到的数据+django框架搭建搜索网站（此部分代码将在以后上传）
</pre>

**PS：使用此代码前，需创建mysql数据库，详见ArticleSpider/settings.py**
