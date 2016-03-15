from urllib.request import urlopen
from bs4 import BeautifulSoup
id = 1
url = "https://mansion-market.com/mansions/detail/{id}".format(id=id)
print(url)
f = urlopen(url)

soup = BeautifulSoup(f)
print(soup.title.string)

# title = soup.find_one('//*[@id="contents"]/div/section/div/div[1]/h1')
title = soup.find_one('h1', class_='title')
print(title)
address = soup.find_one('#contents > div > section > div > div.pullLeft > div.information2 > span.address.iconWrap > span')
print(address)
built_year = soup.find_one('span', class_='year')
print(built_year)
price = soup.find_one('', class_='')

day = soup.find_one('', class_='')

floor_located = soup.find_one('', class_='')

layout = soup.find_one('', class_='')

area = soup.find_one('', class_='')

direction = soup.find_one('', class_='')

