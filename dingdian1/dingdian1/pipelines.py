# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class Dingdian1Pipeline(object):
    def process_item(self, item, spider):
        first_path = "D:\dingdian"
        if not os.path.exists(first_path):
            os.makedirs(first_path)
        novel_path = first_path+"\\"+item["novel_name"]
        if not os.path.exists(novel_path):
            os.mkdir(novel_path)
        chapter_path = novel_path+"\\"+item["chaptername"] +".txt"
        with open(chapter_path,"w") as file:
            file.write(item["chaptername"]+"\n")
            file.write(item["content"]+"\n")

        return item





