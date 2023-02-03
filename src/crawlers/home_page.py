from typing import Dict
from bs4 import BeautifulSoup
import urllib.request
import bs4
import random
import time
import numpy as np

def crawl_apps_in_home_page() -> Dict:
    url = f"https://apps.shopify.com"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    apps = []
    block = {
        "content": "",
        "app_name": []
    }
    web_data = soup.find('div',class_='tw-container lg:tw-w-full lg:tw-px-0 tw-flex tw-flex-wrap tw-gap-xl lg:tw-flex-nowrap').find('h2',class_='tw-text-heading-4')
    block["content"] = web_data.text.strip()
    web_data = soup.find('div',class_='tw-container lg:tw-w-full lg:tw-px-0 tw-flex tw-flex-wrap tw-gap-xl lg:tw-flex-nowrap').find_all('a')
    for set_data in range(0,6,1):
        block["app_name"].append(web_data[set_data].text.strip())
    apps.append(block)

    block = {
        "content": "",
        "app_name": []
    }
    web_data = soup.find('section',class_='tw-w-full tw-flex tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-flex-col tw-basis-full md:tw-basis-1/2 lg:tw-basis-1/3').find('h2',class_='tw-text-heading-4')
    block["content"] = web_data.text.strip()
    web_data = soup.find('section',class_='tw-w-full tw-flex tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-flex-col tw-basis-full md:tw-basis-1/2 lg:tw-basis-1/3').find_all('a')
    for set_data in range(0,3,1):
        block["app_name"].append(web_data[set_data].text.strip())
    apps.append(block)
    
    web_data = soup.find_all('section',class_='tw-w-full tw-flex tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-flex-col tw-py-md md:tw-py-lg lg:tw-py-xl')
    for set_data in web_data:
        block = {
            "content": "",
            "app_name": []
        }
        html_data = str(set_data)
        s = BeautifulSoup(html_data, "html.parser")
        data = s.find('h2')
        block["content"] = data.text.strip()
        data = s.find_all('a')
        for set_data in range(0,6,1):
            block["app_name"].append(data[set_data].text.strip())
        apps.append(block)

    return apps
print(crawl_apps_in_home_page())