from typing import Iterable

import scrapy
from scrapy import Request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from ScrapyProject.ScrapyProject.items import AvitoItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ma"]

    def start_requests(self):
        urls = []
        for i in range(0, 1):
            urls.append(f"https://www.avito.ma/fr/maroc/appartements-%C3%A0_louer?o={i+1}")
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for selector in response.xpath('//*[@id="__next"]/div/main/div/div[5]/div[1]/div/div[1]/a'):
            offer_url = selector.xpath('@href').extract_first()
            ville = selector.xpath('div[3]/div[1]/div[1]/div/p/text()').extract_first()

            if offer_url:
                yield scrapy.Request(offer_url, callback=self.parse_offer, meta={'ville': ville})

    def parse_offer(self, response):
        item = AvitoItem()
        item['name'] = response.xpath('//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div['
                                      '1]/div[1]/div[1]/h1/text()').extract_first()
        item['price'] = response.xpath('//*[@id="__next"]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div['
                                       '1]/div[1]/div[2]/p/text()').extract_first()
        item['ville'] = response.meta.get('ville')
        item['url_offer'] = response.url

        for selector in response.xpath('/html/body/div[1]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div['
                                       '3]/div[2]/ol'):
            champs = ['type', 'secteur', 'surface_habitable']
            keys = []
            values = []
            num_elements = len(selector.xpath('.//*'))
            for i in range(num_elements):
                key = selector.xpath(f'li[{i+1}]/span[1]//text()',).extract_first()
                if key in champs:
                    value = selector.xpath(f'li[{i+1}]/span[2]//text()').extract_first()
                    keys.append(key)
                    values.append(value)
            Dict = dict(zip(keys, values))
            item['type'] = Dict.get('type')
            item['secteur'] = Dict.get('secteur')
            item['surface_habitable'] = Dict.get('surface_habitable')

        yield item


def result():
    urls = []

    def crawler_results(item):
        urls.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(AvitoSpider)
    crawler_process.start()
    return urls

if __name__ == '__main__':
    results = result()
