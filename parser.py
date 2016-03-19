import data
import re

class Parser():
    def parse(self, estate):
        estate['築年'] = int(re.sub('\D', '', str(estate.get('築年', '')) + '01'))
        estate['総戸数'] = re.sub('\D', '', estate.get('総戸数', '0'))
        estate['階数'] = re.sub('\D', '', estate.get('階数', '0'))
        estate['都道府県'] = self.extract_pref(estate.get('住所', ''))
        estate['所在地1'] = self.extract_city(
            estate.get('住所', ''), estate.get('都道府県', ''))
        floor_located = estate.get('所在階', '')
        if (floor_located == ''):
           estate['所在階'] = ''
        else:
            estate['所在階'] = int(re.sub('\D', '', floor_located))
        estate['間取り'] = estate.get('間取り', '')
        estate['専有面積'] = re.sub('[^.^0-9]', '', estate.get('専有面積', ''))
        estate['方角'] = estate.get('方角', '')
        return estate

    def extract_pref(self, address):
        for pref in data.PREF_TABLE.values():
            if (address.count(pref) == 1):
                return pref

    def extract_city(self, address, pref):
        for city in data.CITY_TABLE[pref].values():
            if (address.count(city) == 1):
                return city


