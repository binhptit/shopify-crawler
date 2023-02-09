import urllib
from bs4 import BeautifulSoup
from .utils import read_json, get_data_from_soup
import time
import random
from typing import List
import logging
from .decorators import time_log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@time_log
def subcategory_drop_shipping(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    result_dict = {
        "home_page":{
            "recommend": [],
        },
        "tags": {
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_dict["home_page"]["recommend"] = get_data_from_soup(web_data)
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_dict["home_page"]["recommend"] += get_data_from_soup(web_data)

    return result_dict

@time_log
def subcategory_print_on_demand(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in result_dict.keys():
        page_number = 1
        while True:
            logging.info("Crawling page {} with sort mode {}".format(page_number, sort_mode))
            url = base_url + f'?page={page_number}&sort_by={sort_mode}'

            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
            result_from_soup : List[str] = get_data_from_soup(web_data)
            result_dict[sort_mode] += result_from_soup
            
            if not len(web_data) or not len(result_from_soup):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

@time_log
def subcategory_buying_wholesale(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in result_dict.keys():
        page_number = 1
        while True:
            logging.info("Crawling page {} with sort mode {}".format(page_number, sort_mode))
            url = base_url + f'?page={page_number}&sort_by={sort_mode}'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
            result_from_soup : List[str] = get_data_from_soup(web_data)
            result_dict[sort_mode] += result_from_soup
                
            if not len(web_data) or not len(result_from_soup):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

@time_log
def subcategory_finding_suppliers(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in result_dict.keys():
        page_number = 1
        while True:
            logging.info("Crawling page {} with sort mode {}".format(page_number, sort_mode))
            url = base_url + f'?page={page_number}&sort_by={sort_mode}'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
            result_from_soup : List[str] = get_data_from_soup(web_data)
            result_dict[sort_mode] += result_from_soup
            
            if not len(web_data) or not len(result_from_soup):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

@time_log
def crawl_category_finding_products():
    link_dict = read_json("src/crawlers/configs/link_config.json")

    page = urllib.request.urlopen(link_dict["categories"]["finding-products"])
    soup = BeautifulSoup(page, 'html.parser')

    result_dict = {
        "finding-products": {
            "recommend": [],
        },
        "subcategory":{
            "drop-shipping": subcategory_drop_shipping(link_dict["subcategories"]["drop-shipping"]),
            "print-on-demand": subcategory_print_on_demand(link_dict["subcategories"]["print-on-demand-pod"]),
            "buying-wholesale": subcategory_buying_wholesale(link_dict["subcategories"]["buying-wholesale"]),
            "finding-suppliers": subcategory_finding_suppliers(link_dict["subcategories"]["finding-suppliers"]),
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[str] = get_data_from_soup(web_data)
    result_dict["finding-products"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[str] = get_data_from_soup(web_data)
    result_dict["finding-products"]["recommend"] += result_from_soup

    return result_dict
