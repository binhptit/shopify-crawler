import urllib
from bs4 import BeautifulSoup
import bs4
import time
import random
from typing import List, Dict
import logging
from .decorators import time_log 
import json 
import requests

def get_request(url, proxy):
    logging.info(f"Start get_request---- {url} using proxy: {proxy}")
    try:
        with requests.Session() as session:
            response = session.get(url, proxies={'http': f"http://{proxy}"})
            return response.text
    except Exception as e:
        response = urllib.request.urlopen(url)
        print("Exception:", e)

    return response

def filter_string(string: str, characters: str) -> str:
    return ''.join([c for c in string if c in characters])

def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return json.load(infile)

link_dict = read_json("src/crawlers/configs/link_config.json")

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

def get_info_app_thumbnail(web_data):
    info_app_dict = {}

    info_app_dict['app_name'] = str(web_data.text.strip())
    info_app_dict['slug'] = str(web_data.find('a').get('href')).split('?')[0].split('/')[-1]
    
    return info_app_dict


def get_data_from_soup(web_data):
    text_results = []
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                text_results.append(get_info_app_thumbnail(result_set_data))
    else:
        if web_data.text.strip():
            text_results.append(get_info_app_thumbnail(web_data))
    
    return text_results

def palindrom_number(number):
    return str(number) == str(number)[::-1]

@time_log
def template_crawl_grid_apps(base_url, proxy_pool, top_k = 10000):
    # logging.info("Template crawl grid apps at %s", base_url)
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in result_dict.keys():
        proxy = proxy_pool.get_proxy()

        page_number = 1
        while True:
            # logging.info("Crawling page {} with sort mode {}".format(page_number, sort_mode))
            url = base_url + f'?page={page_number}&sort_by={sort_mode}'

            # page = urllib.request.urlopen(url)

            page = get_request(url, proxy)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
            result_from_soup : List[Dict] = get_data_from_soup(web_data)
            result_dict[sort_mode] += result_from_soup

            time.sleep(random.randint(2, 5))

            if not len(web_data) or not len(result_from_soup) or len(result_dict[sort_mode]) >= top_k:
                break
            
            page_number += 1
        
        proxy_pool.put_proxy(proxy)

    return result_dict

def get_data(page, subcategory_name, proxy_pool):
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "recommend": [],
        "tags": {
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_dict["recommend"] = get_data_from_soup(web_data)
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_dict["recommend"] += get_data_from_soup(web_data)

    for tag in link_dict['subcategories'][subcategory_name]['tags'].keys():
        result_dict['tags'][tag] = template_crawl_grid_apps(link_dict['subcategories'][subcategory_name]['tags'][tag], proxy_pool=proxy_pool)

    return result_dict

@time_log
def subcategory_crawler(subcategory_name, proxy_pool):
    # logging.info("Crawling subcategory_crawler: {}...".format(subcategory_name))
    url = link_dict["subcategories"][subcategory_name]["url"]

    proxy = proxy_pool.get_proxy()

    try:
        with requests.Session() as session:
            response = session.get(url, proxies={'http': f"http://{proxy}"})
            page = response.text
    
        result_dict = get_data(page, subcategory_name, proxy_pool)
        proxy_pool.put_proxy(proxy)
    except Exception as e:
        response = urllib.request.urlopen(url)
        result_dict = get_data(response, subcategory_name, proxy_pool)
        print("Exception:", e)

    return result_dict

def keep_number(number):
    return ''.join([c for c in number if c.isdigit()])