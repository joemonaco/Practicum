from bs4 import BeautifulSoup as BS
import urllib
import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


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
time.sleep(10)

# Get rid of all ascii characters
page_text = driver.page_source.encode('utf-8').decode('ascii', 'ignore')
soup = BS(page_text, 'html.parser')

# Write the html file
htmlFile = open('index.html', 'w')
htmlFile.write(soup.prettify())
htmlFile.close()
