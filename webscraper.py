import requests
from bs4 import BeautifulSoup
import json

with open("guns.json",  "w", encoding='utf-8') as file:
     file.write('[\n')
     for y in range(1, 3):
         c1 = (y-1)*20
         URL = f'https://www.genitron.com/Handguns/Search-Results/Any/Any/Any/Any/0/0/0/0/{y}'
         page = requests.get(URL)
         soup = BeautifulSoup(page.content, 'html.parser')
         gun_links = soup.select('.result-list-item')
         urls = [f'https://www.genitron.com{tag["href"]}' for tag in gun_links]
         for i in range(0, len(urls)):
             detail_page = requests.get(urls[i], headers={'User-agent': 'Mozilla/5.0'})
             dsoup = BeautifulSoup(detail_page.content, 'html.parser')
             names = dsoup.select('.table:nth-child(1) td:nth-child(1)')
             types = dsoup.select('.specrow:nth-child(1) td:nth-child(2)')
             man = dsoup.select('.table:nth-child(1) td:nth-child(1)')
             trigger = dsoup.select('.specrow:nth-child(5) td:nth-child(2)')
             length = dsoup.select('.mCell')
             barrel_length = dsoup.select('.mCell')
             weight = dsoup.select('.specrow td:nth-child(4)')
             magazine = dsoup.select('.specrow:nth-child(7) td:nth-child(2)')
             row = f' "id": {c1 + i + 1},\n "name": "{names[0].text}",\n "type": "{types[0].text}",\n "manufacturer": "{man[0].text}",' \
                   f'\n "trigger": "{trigger[1].text}",\n "length": "{length[0].text}",\n "barrel_length": "{barrel_length[1].text}"' \
                   f',\n "weight": "{weight[1].text}",\n "magazine": "{magazine[0].text}",\n "url": "{urls[i]}"'
             row = '{\n' + row + '\n}, '
             print(row)
             file.write(row)
     file.write(']')