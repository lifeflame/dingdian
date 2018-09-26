# -*- coding: utf-8 -*-
# Python 3.6

import scrapy
from dingdian1.items import Dingdian1Item

class Myspider(scrapy.Spider):

    name = "dingdian1"
    #指定可爬url的域名
    allowed_domains = ["www.23us.so"]
    #生成开始爬网的url列表
    start_urls = ["https://www.23us.so/list/"+str(i)+"_1.html" for i in range(1, 10)]

    def parse(self, response):
        #获取网页中最大翻页数，利用for循环得到所有的可爬url地址
        max_int = response.xpath("//div[@id='pagelink']/a[last()]/text()").extract()[0]
        baseurl = response.url[:-6]
        # for i in range(1, 2):
        for i in range(1,int(max_int)+1):
            url = baseurl+str(i)+".html"
            yield scrapy.Request(url,callback=self.get_name)

    """
    至此，以上我们就得到了网站所有的可爬url地址
    """
    def get_name(self,response):
        #以下几行是为了获取小说的name,还有小说地址
        tds = response.xpath("//tr[@bgcolor='#FFFFFF']")
        for td in tds:
            novel_name = td.xpath("./td[1]/a/text()").extract()[0]
            novel_url = td.xpath("./td[1]/a/@href").extract()[0]
            if novel_url:
                #我们需要把name和url信息传递给回调函数，需要用到meta.
                yield scrapy.Request(novel_url,callback=self.get_novel_content,meta={"name":novel_name,
                                                                                   "novelurl":novel_url})

    def get_novel_content(self,response):
        #调用meta的方式
        novel_name = response.meta["name"]
        #在小说简介处获取作者以及具体章节的url，然后接着传递。
        author = response.xpath("string(//table[@id='at']//td[2])").extract()[0].replace("\xa0","")
        novelurl = response.url
        name_id = novelurl[-9:-5]
        chapterlisturl = response.xpath("//p[@class='btnlinks']/a[@class='read']/@href").extract()[0]
        yield scrapy.Request(chapterlisturl,callback=self.get_chapter_content,meta={"novel_name":novel_name,
                                                                                    "author":author,
                                                                                    "name_id":name_id})

    def get_chapter_content(self,response):
        novel_name = response.meta["novel_name"]
        author = response.meta["author"]
        name_id = response.meta["name_id"]
        #注意，一定要将tbody标签去掉
        for chapters in response.xpath("//table[@id='at']/tr"):
            for chapter in chapters.xpath("./td"):
                chapterurl = chapter.xpath("./a/@href").extract()[0]
                # print(chapterurl)
                chaptername = chapter.xpath("./a/text()").extract()[0]
                yield scrapy.Request(chapterurl,callback=self.get_content,meta={"novel_name":novel_name,
                                                                                "author":author,
                                                                                "name_id":name_id,
                                                                                "chaptername":chaptername})

    def get_content(self,response):
        #获取具体章节小说的文字内容，并将其存入在item中
        item = Dingdian1Item()
        item["novel_name"] = response.meta["novel_name"]
        item["author"] = response.meta["author"]
        item["name_id"] = response.meta["name_id"]
        item["chaptername"] = response.meta["chaptername"]
        # print(type(item["chaptername"]))
        content = response.xpath("string(//dd[@id='contents'])")[0].extract().replace("\xa0","").replace("\r\n","")
        print(content)
        item["content"] = content
        yield item








