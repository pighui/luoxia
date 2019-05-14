# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from luoxia import settings


class LuoxiaPipeline(object):
    def process_item(self, item, spider):
        title= item['title']
        bookname = item['bookname']
        titlename = item['titlename']
        text = item['text']
        path = "books/%s/%s/" % (title, bookname)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+titlename+'.txt', 'a', encoding='utf-8') as f:
            f.write(text)
        return item

class LuoxiaImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield Request(url, meta={'title': item['title'],
                                     'bookname': item['bookname']})

    def item_completed(self, results, item, info):
        # 将下载完成后的图片路径设置到item中
        item['images'] = [x for ok, x in results if ok]
        return item

    def file_path(self, request, response=None, info=None):
        # 为每本书创建一个目录，存放她自己所有的图片
        title = request.meta['title']
        bookname = request.meta['bookname']
        book_dir = os.path.join(settings.IMAGES_STORE, title +'/'+ bookname)
        if not os.path.exists(book_dir):
            os.makedirs(book_dir)
        # 从连接中提取扩展名
        try:
            ext_name = request.url.split(".")[-1]
        except:
            ext_name = 'jpg'
        # 返回的相对路径
        return '%s/%s/%s.%s' % (title, bookname, bookname, ext_name)