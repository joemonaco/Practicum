
from bs4 import BeautifulSoup as BS
import urllib
import requests

url = 'http://njcaa.org/sports/bsb/2018-19/div1/teams/arizonawesterncollege?view=lineup'
result = requests.get(url)
c = result.content
soup = BS(c)
print(soup)