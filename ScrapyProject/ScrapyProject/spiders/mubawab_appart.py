import scrapy
from scrapy import Request
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher


class MubawabAppartSpider(scrapy.Spider):
    name = "mubawab_appart"
    allowed_domains = ["mubawab.ma"]

    def start_requests(self):
        for i in range(0, 300):
            url = f"https://www.mubawab.ma/fr/sc/appartements-a-louer:p:{i+1}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for selecor in response.xpath('/html/body/section/div[2]/div[3]/ul/li'):
            offer_url = selecor.xpath('@linkref').extract_first()

            if offer_url:
                yield scrapy.Request(url=offer_url, callback=self.parse_offer)

    def parse_offer(self, response):
        name = response.xpath('/html/body/section/div[2]/div/div[1]/h1//text()').extract_first()
        price = response.xpath('/html/body/section/div[2]/div/div[1]/div[1]/div[1]/h3//text()').extract_first()
        secteurEtVille = response.xpath('/html/body/section/div[2]/div/div[1]/h3//text()').extract_first()
        surface = response.xpath('/html/body/section/div[2]/div/div[1]/div[2]/span[1]//text()').extract_first()

        yield {
            'name': name,
            'url_offer': response.url,
            'price': price,
            'Type': 'Appartement',
            'Secteur et Ville': secteurEtVille,
            'Surface': surface
        }

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