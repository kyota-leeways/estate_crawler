import data
import re

class Parser():
    def parse(self, estate):
        # estate['築年'] = int(re.sub('\D', '', str(estate.get('築年', '')) + '01'))
        estate['築年月'] = self.parseBuiltYear(estate.get('築年月', ''))
        estate['総戸数'] = int(re.sub('\D', '', str(estate.get('総戸数', 0))))
        estate['階数'] = int(re.sub('\D', '', str(estate.get('階数', 0))))
        estate['都道府県'] = self.extract_pref(estate.get('住所', ''))
        estate['所在地1'] = self.extract_city(
        estate.get('住所', ''), estate.get('都道府県', ''))
        floor_located = estate.get('所在階', '')
        if (floor_located == ''):
            estate['所在階'] = ''
        else:
            estate['所在階'] = int(re.sub('\D', '', floor_located))
        estate['徒歩分数'] = self.parseWalkTime(estate.get('交通'))
        estate['間取り'] = estate.get('間取り', '')
        estate['専有面積'] = float(re.sub('[^.^0-9]', '', str(estate.get('専有面積', '0'))))
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

    def parseWalkTime(self, railway_info):
        """
        交通情報から最寄り駅の徒歩分数を取得
        :param railway_info:
        :return:
        """
        walk_time = re.sub('\D', '', railway_info)
        walk_time = int(walk_time)
        print(walk_time)
        return walk_time

    def parseBuiltYear(self, built_year_str: str):
        """
        築年 の文字列を パースして6桁の数値にする.
        """
        built_year_arr = re.split('\D', built_year_str)
        if (type(built_year_str) is int):
            return built_year_str
        elif (len(built_year_arr) == 1):
            return int(built_year_str)
        # month
        if (len(built_year_arr[1]) == 1):
            built_year_arr[1] = '0' + built_year_arr[1]
        # day
        if (len(built_year_arr[2]) == 0):
            built_year_arr[2] = '01'
        elif (len(built_year_arr[2]) == 1):
            built_year_arr[2] += '0' + built_year_arr[2]

        built_year = ''.join(built_year_arr)
        return built_year


