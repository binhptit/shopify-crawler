from bs4 import BeautifulSoup
import bs4
from typing import Dict
import urllib.request
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import time

def Crawl_Best_Match(html) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')
    List_app = []
    web_data = soup.find('main',class_="tw-grow").find_all('div',class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    link = str(web_data)
    soup = BeautifulSoup(link, 'html.parser')
    web_data = soup.find_all('a')
    for set_data in web_data:
        List_app.append(set_data.text.strip())
    return List_app

page = 1
start_time = time.time()
while True:
    browser = webdriver.Chrome(executable_path="./chromedriver.exe")

    browser.get(f"https://apps.shopify.com/search?q=tiktok+pixel&sort_by=popular&page={page}")
    html = browser.page_source

    with open(f"data/website_{page}.html", "w", encoding='utf-8') as file:
        file.write(html)
    sleep(0)
    
    res = Crawl_Best_Match(html)
    print(res)
    if not len(res):
        break
    
    page += 1
print(start_time-time.time())