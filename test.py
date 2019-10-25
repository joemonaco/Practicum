from bs4 import BeautifulSoup as BS
import urllib
import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime as DT
import csv


url = 'http://cloud.rapsodo.com/2.1/#/auth/login'
result = requests.get(url)
c = result.content

# SELENIUM
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

driver.find_element_by_id('username').send_keys('ccollazo@monmouth.edu')
driver.find_element_by_id('password').send_keys('mubaseball')
driver.find_element_by_class_name('auth-button').click()

url = 'http://cloud.rapsodo.com/2.1/#/team-stats'

driver.get(url)
driver.find_element_by_id('ngb-tab-2').click()
time.sleep(10)

# Get rid of all ascii characters
page_text = driver.page_source.encode('utf-8').decode('ascii', 'ignore')
soup = BS(page_text, 'html.parser')

# Grabbing all picthers by taking spans from site
allPitchers = soup.findAll('span', class_=[])

pitcherData = []
allPitcherData = []


# loop through allPitchers and grab pitcher name by doing count%6
for span in allPitchers:
    allPitcherData.append(str(span.get_text().strip()))

# loop thr
count = 0
for pitcher in allPitcherData:
    if len(pitcher) > 3 and pitcher != 'Starter':

        pitcherDict = {'name': allPitcherData[count], 'throws': allPitcherData[count+2], 'height': allPitcherData[count+3],
                       'weight': allPitcherData[count+4], 'age': allPitcherData[count+5]}
        pitcherData.append(pitcherDict)

    count = count + 1


print pitcherData


# Grab keys to be the headers of the csv and create the csv file based on dictionary
keys = pitcherData[0].keys()
with open('pitcher.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(pitcherData)

# Write the html file
# time = DT.now()
# htmlFile = open(str(time) + '.html', 'w')
# htmlFile.write(soup.prettify())
# htmlFile.close()
