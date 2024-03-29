import scrapy
from scrapy import Request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from ScrapyProject.ScrapyProject.items import MubawabItem


class MubawabAppartSpider(scrapy.Spider):
    name = "mubawab_appart"
    allowed_domains = ["mubawab.ma"]
    custom_settings = {
        'ITEM_PIPELINES': {'ScrapyProject.ScrapyProject.pipelines.MubawabPipeline': 100}
    }

    def start_requests(self):
        for i in range(0, 2):
            url = f"https://www.mubawab.ma/fr/sc/appartements-a-louer:p:{i+1}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for selecor in response.xpath('/html/body/section/div[2]/div[3]/ul/li'):
            offer_url = selecor.xpath('@linkref').extract_first()

            if offer_url:
                yield scrapy.Request(url=offer_url, callback=self.parse_offer)

    def parse_offer(self, response):
        item = MubawabItem()
        item['url_offer'] = response.url
        item['name'] = response.xpath('/html/body/section/div[2]/div/div[1]/h1//text()').extract_first()
        item['price'] = response.xpath('/html/body/section/div[2]/div/div[1]/div[1]/div[1]/h3//text()').extract_first()
        item['secteur_et_ville'] = response.xpath('/html/body/section/div[2]/div/div[1]/h3//text()').extract_first()
        item['surface'] = response.xpath('/html/body/section/div[2]/div/div[1]/div[2]/span[1]//text()').extract_first()
        item['type'] = 'Appartement'

        yield item

def result():
    urls = []

    def crawler_results(item):
        urls.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(MubawabAppartSpider)
    crawler_process.start()
    return urls

if __name__ == '__main__':
    results = result()