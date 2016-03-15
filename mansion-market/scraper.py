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


