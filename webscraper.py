import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.genitron.com/Handguns/Search-Results/Any/Any/Any/Any/0/0/0/0/1'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
gun_links = soup.select('.result-list-item')
names = [tag.text for tag in gun_links]
man = []
urls = [f'https://www.genitron.com/{tag["href"]}' for tag in gun_links]

print(urls)

with open("guns.json",  "w", encoding='utf-8') as file:
     file.write('[\n')
     for i in range(0, 20):
         detail_page = requests.get(urls[i], headers={'User-agent': 'Mozilla/5.0'})
         dsoup = BeautifulSoup(detail_page.content, 'html.parser')
         types = dsoup.select('.specrow:nth-child(1) td:nth-child(2)')
         print(types[0].text)
#         print(vyrobce)
#
         row = f'"types": "{types[0].text}"'
#         # row = f'"id": {i + 1}, "name": "{names[i]}", "types": "{types[0].text [i}", "manufacturer": "{man[i]}", "trigger": "{trigger[i]}"' \
#         #       f' "length": "{length[i]}", "barrel_length": "{barrel_length[i]}", "weight": "{weight[i]}"' \
#         #       f' "magazine": "{magazine[i]}","url": "{urls[i]}"'
#         # row = '{' + row + '}, '
#         print(row)
         file.write(row)
         file.write(']')