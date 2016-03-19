from urllib.request import urlopen
from bs4 import BeautifulSoup
import data
from parser import Parser
import re
import pymongo
import datetime
import time
# from BeautifulSoup import BeautifulSoup


def scrape(html_file):
    soup = BeautifulSoup(html_file, 'lxml')
    print(soup.title.string)
    get_date = int(datetime.datetime.now().strftime('%Y%m%d'))
    estate_base = {'取得元': 'mansion-market', '取得日': get_date}
    # 物件名
    estate_name = soup.find('h1', class_='title').string
    estate_base['物件名'] = estate_name
    # マンション詳細情報
    details = soup.find('table', class_='tableDotted').findAll('td')
    # print(details)
    # detail_keys = {1: 'address', 2: 'built_year', 3: 'number_of_houses',
    #                # 4: 'railways',
    #                5: 'number_of_floors', 6: 'building_structure',
    #                9: 'use_district_1'}
    detail_keys = {1: '住所', 2: '築年', 3: '総戸数',
                   # 4: 'railways',
                   5: '階数', 6: '建物構造',
                   9: '用途地域'}
    for i, key in detail_keys.items():
        estate_base[key] = details[i].string

    estate_base = estate_parser.parse(estate_base)

    each_estates = soup.find_all('li', class_='contentsInner')
    # print(each_estates)
    for i, estate_info in enumerate(each_estates):
        # 物件
        estate = estate_base.copy()
        # print(estate_info)
        # 価格
        price = estate_info.find('p', class_='price').string
        price = re.sub('\D', '', price) + '0000'
        price = int(price)
        estate['価格'] = price
        # 更新日
        updated_at = estate_info.find('p', class_='date').string
        updated_at = re.sub('\D', '', updated_at) + '01'
        updated_at = int(updated_at)
        estate['変更日'] = updated_at
        details = estate_info.find('ul', class_='condition').find_all('li')
        # detail_keys = ['floor_located', 'layout', 'occupation_area', 'direction']
        detail_keys = ['所在階', '間取り', '専有面積', '方角']
        for i, detail in enumerate(details):
            key = detail_keys[i]
            estate[key] = detail.string
            # print(estate[key])
        estate = estate_parser.parse(estate)
        print(estate)
        # 物件の保存
        client = pymongo.MongoClient()
        db = client['crawled_data']
        collection = db['estates']
        try:
            collection.insert(estate)
        except pymongo.errors.DuplicateKeyError as e:
            print("Duplicate estate", estate)
            continue

ids = range(100, 28800)
estate_parser = Parser()

for id in ids:
    url = "https://mansion-market.com/mansions/detail/{id}".format(id=id)
    f = urlopen(url)
    scrape(f)
    time.sleep(1)
