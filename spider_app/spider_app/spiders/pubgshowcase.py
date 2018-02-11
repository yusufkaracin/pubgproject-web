# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime

from scrapy.spiders import CrawlSpider
import requests
from json_environ import Environ

SPIDER_APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(SPIDER_APP, '..', '..', '.env.json')

env = Environ(path=ENV_PATH)

DEBUG = env("DEBUG", default=True)

PUBGSHOWCASE_DOMAIN = "https://pubgshowcase.com"
NEED_A_KEY = "need a key"
LI_INDEX_FOR_NEED_KEY = 3
DIV_INDEX_FOR_CRATE_IMG = 2
DIV_INDEX_FOR_CRATE_ID = 1
DIV_INDEX_FOR_ITEM_IMG = 3
DIV_INDEX_FOR_ITEM_DROP_RATE = 3
DIV_INDEX_FOR_ITEM_NAME = 1


class PubgshowcaseSpider(CrawlSpider):
    name = 'pubgshowcase'
    allowed_domains = ['pubgshowcase.com']
    start_urls = ['https://pubgshowcase.com/containers.php?id=All&type=Crates']

    def __init__(self, *args, **kwargs):
        self.data = []
        if DEBUG:
            self.data = self.get_test_data()
            self.start_urls = []
        super(PubgshowcaseSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def get_test_data():
        json_file = os.path.join(SPIDER_APP, '..', 'test_response.json')
        with open(json_file, mode='r+') as f:
            data = json.loads(f.read())
        return data

    @staticmethod
    def need_key(response):
        text = (
            response.xpath(
                query='//ul[contains(@style, "margin-bottom:0px;")]/li[$i]/span/strong/a/text()',
                i=LI_INDEX_FOR_NEED_KEY
            )
            .extract_first()
        )

        return text == NEED_A_KEY

    @staticmethod
    def get_item_name(skin_item_selector):
        item_name = skin_item_selector.xpath('div[$i]/h4/a/text()', i=DIV_INDEX_FOR_ITEM_NAME).extract_first()
        return item_name

    @staticmethod
    def get_item_drop_rate(skin_item_selector):
        drop_rate = skin_item_selector.xpath('div[$i]/a/span/text()', i=DIV_INDEX_FOR_ITEM_DROP_RATE).extract_first()
        if not drop_rate:
            return

        drop_rate = drop_rate.rstrip('%')
        drop_rate = float(drop_rate)
        return drop_rate

    @staticmethod
    def get_item_img(skin_item_selector, crate=False):
        div_index = DIV_INDEX_FOR_CRATE_IMG if crate else DIV_INDEX_FOR_ITEM_IMG
        img = skin_item_selector.xpath('div[$i]/a/img/@src', i=div_index).extract_first()
        if not img:
            return ''

        return "{}/{}".format(PUBGSHOWCASE_DOMAIN.rstrip('/'), img.lstrip('/'))

    @staticmethod
    def get_steam_data(skin_item_selector):
        price_selector = skin_item_selector.xpath('div[contains(@class, "caption")]/p[1]/a[2]')
        steam_url = price_selector.xpath('@href').extract_first()
        steam_price = price_selector.xpath('text()').extract()[-1]
        steam_price = round(float(steam_price), 3)

        return steam_url, steam_price

    @staticmethod
    def get_crate_id(skin_item_selector):
        href = skin_item_selector.xpath('div[$i]/h4/a/@href', i=DIV_INDEX_FOR_CRATE_ID).extract_first()
        crate_id = href.split('?id=')[-1]
        return int(crate_id)

    @staticmethod
    def get_crate_detail_url(crate_id):
        return '/containers.php?id={}'.format(crate_id)

    def parse_crate_detail(self, response):
        crate = response.meta.pop('crate')
        crate['items'] = []
        created_at = str(datetime.now())

        crate['need_key'] = self.need_key(response=response)
        crate['created_at'] = created_at
        for skin_item in response.xpath('//div[contains(@class, "skin-item")]'):
            steam_url, steam_price = self.get_steam_data(skin_item_selector=skin_item)
            name = self.get_item_name(skin_item_selector=skin_item)
            url = ''
            if name:
                url = "{}/skin.php?item={}".format(PUBGSHOWCASE_DOMAIN.rstrip('/'), name)
            item_data = {
                'name': name,
                'url': url,
                'drop_rate': self.get_item_drop_rate(skin_item_selector=skin_item),
                'img': self.get_item_img(skin_item_selector=skin_item),
                'steam_url': steam_url,
                'steam_price': steam_price,
                'created_at': created_at,
            }
            crate['items'].append(item_data)

        self.data.append(crate)
        yield crate

    def parse(self, response):
        for crate_div in response.xpath('//div[contains(@class, "skin-item")]'):
            steam_url, steam_price = self.get_steam_data(skin_item_selector=crate_div)
            crate_id = self.get_crate_id(skin_item_selector=crate_div)
            url = "{}{}".format(PUBGSHOWCASE_DOMAIN.rstrip('/'), self.get_crate_detail_url(crate_id))
            crate = {
                'id': crate_id,
                'name': self.get_item_name(skin_item_selector=crate_div),
                'url': url,
                'img': self.get_item_img(skin_item_selector=crate_div, crate=True),
                'steam_url': steam_url,
                'steam_price': steam_price,
            }

            yield response.follow(
                url=url,
                callback=self.parse_crate_detail,
                meta={'crate': crate}
            )

    def close(self, spider, reason):
        if reason == "shutdown":
            return

        token = "Bearer {}".format(env("SECRET_KEY", default="kminvupn=7dbw70e!#njo8qas2bx$tmw$nv1pt$g30&+f4(8c)"))
        headers = {'Authorization': token}
        url = env("SPIDER_CALLBACK", default="http://0.0.0.0:8080/spider")
        requests.post(url, json=self.data, headers=headers)
