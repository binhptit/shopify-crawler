from bs4 import BeautifulSoup
import bs4
from typing import Dict
import urllib.request
import requests
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import time
import random

def crawl_best_match(html) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')
    list_app = []
    web_data = soup.find('main',class_="tw-grow").find_all('div',class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    link = str(web_data)
    soup = BeautifulSoup(link, 'html.parser')
    web_data = soup.find_all('a')
    for set_data in web_data:
        list_app.append(set_data.text.strip())

    return list_app

def crawl_searching_result(input_query) -> Dict:
    result = {
        'best_match': [],
        'popular': [],
        'newest': []
    }
    preprocessed_input_query = '+'.join(input_query.split(' '))

    for mode_sort in ['popular', 'best_match', 'newest']:
        page = 1
        while True:
            browser = webdriver.Chrome(executable_path="chromedriver")

            browser.get(f"https://apps.shopify.com/search?q={preprocessed_input_query}&sort_by={mode_sort}&page={page}")
            html = browser.page_source
            browser.close()

            sleep(random.randint(0, 3))
            try:
                apps = crawl_best_match(html)
            except Exception as e:
                print(f"Ignore result page {page}, sort mode {mode_sort} due to Exception: ", e)
                continue
            
            result[mode_sort].extend(apps)

            if not len(apps):
                break
            
            page += 1
    
    return result
