# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

# useful for handling different item types with a single interface
import scrapy


class AvitoPipeline(object):
    def process_item(self, item, spider):
        return item


class MubawabPipeline:
    def process_item(self, item, spider):
        if 'name' in item:
            item['name'] = item['name'].replace('\t', '').replace('\n', '').replace("\xa0", '')
        if 'price' in item:
            item['price'] = item['price'].replace('\t', '').replace('\n', '').replace("\xa0", '')
            item['price'] = item['price'].split(' ')[0]
        if 'secteur_et_ville' in item:
            item['secteur_et_ville'] = item['secteur_et_ville'].replace('\t', '').replace('\n', '').replace("\xa0", '')
            try:
                parts = item['secteur_et_ville'].split('à')
                item['secteur'], item['ville'] = parts[0].strip(), parts[1].strip()
            except:
                item['secteur'] = None
                item['ville'] = item['secteur_et_ville'].strip()
            del item['secteur_et_ville']
        if 'surface' in item:
            item['surface'] = item['surface'].replace('\t', '').replace('\n', '').replace("\xa0", '')

        return item
