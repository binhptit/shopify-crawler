from bs4 import BeautifulSoup
import bs4
from typing import Dict
from selenium import webdriver
from time import sleep
import time
import random
import logging
from selenium.webdriver.chrome.options import Options
from utilities.utils import keep_number

def crawl_best_match(html) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')
    list_app = []
    web_data = soup.find('main',class_="tw-grow").find_all('div',class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    link = str(web_data)
    soup = BeautifulSoup(link, 'html.parser')
    web_data = soup.find_all('a')
    for set_data in web_data:
        list_app.append(set_data.text.strip())

    web_data = soup.find_all('span', class_='tw-inline tw-self-center tw-text-body-md--mobile md:tw-text-body-md--desktop tw-text-fg-tertiary')
    try:
        number_of_apps = int(keep_number(web_data.text))
    except:
        number_of_apps = 0

    return list_app, number_of_apps

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
            logging.info('Crawling page {} with sort mode {}!'.format(page, mode_sort))
            
            # Set the Chrome options to run in headless mode
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            browser = webdriver.Chrome(executable_path="./assets/chromedriver", chrome_options=chrome_options)
            sleep(random.randint(1, 2))
            browser.get(f"https://apps.shopify.com/search?q={preprocessed_input_query}&sort_by={mode_sort}&page={page}")
            html = browser.page_source
            browser.close()

            sleep(random.randint(0, 3))
            try:
                apps, total_apps = crawl_best_match(html)
            except Exception as e:
                print(f"Ignore result page {page}, sort mode {mode_sort} due to Exception: ", e)
                continue
            
            result[mode_sort].extend(apps)

            if not apps:
                if len(result[mode_sort]) < total_apps:
                    logging.warning('Crawling result is not enough!')
                break
            
            page += 1
    
    return result
