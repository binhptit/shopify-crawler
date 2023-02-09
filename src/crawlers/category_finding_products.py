import urllib
from bs4 import BeautifulSoup
import bs4
from .utils import read_json
import time
import random

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
    
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                result_dict["home_page"]["recommend"].append(result_set_data.text.strip())
    else:
        result_dict["home_page"]["recommend"].append(web_data.text.strip())
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                result_dict["home_page"]["recommend"].append(result_set_data.text.strip())
    else:
        result_dict["home_page"]["recommend"].append(web_data.text.strip())

    return result_dict

def subcategory_print_on_demand(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in ["popular", "best_match", "newest"]:
        page_number = 1
        while True:
            url = base_url + '?page={page_number}&sort_by={sort_mode}'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    
            if isinstance(web_data, bs4.element.ResultSet):
                for result_set_data in web_data:
                    if result_set_data.text.strip():
                        result_dict[sort_mode].append(result_set_data.text.strip())
            else:
                result_dict[sort_mode].append(web_data.text.strip())
            
            if not len(web_data) or len(result_dict[sort_mode]):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

def subcategory_buying_wholesale(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in ["popular", "best_match", "newest"]:
        page_number = 1
        while True:
            url = base_url + '?page={page_number}&sort_by={sort_mode}'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    
            if isinstance(web_data, bs4.element.ResultSet):
                for result_set_data in web_data:
                    if result_set_data.text.strip():
                        result_dict[sort_mode].append(result_set_data.text.strip())
            else:
                result_dict[sort_mode].append(web_data.text.strip())
                
            if not len(web_data) or len(result_dict[sort_mode]):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

def subcategory_finding_suppliers(base_url, top_k = 10):
    result_dict = {
        "popular": [],
        "best_match": [],
        "newest": []
    }

    for sort_mode in ["popular", "best_match", "newest"]:
        page_number = 1
        while True:
            url = base_url + '?page={page_number}&sort_by={sort_mode}'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            web_data = soup.find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    
            if isinstance(web_data, bs4.element.ResultSet):
                for result_set_data in web_data:
                    if result_set_data.text.strip():
                        result_dict[sort_mode].append(result_set_data.text.strip())
            else:
                result_dict[sort_mode].append(web_data.text.strip())
                
            if not len(web_data) or len(result_dict[sort_mode]):
                break
            
            time.sleep(random.randint(0, 2))
            page_number += 1

    return result_dict

def crawl_category_finding_products():
    link_dict = read_json("src/crawlers/link_config.json")

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
    
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                result_dict["finding-products"]["recommend"].append(result_set_data.text.strip())
    else:
        result_dict["finding-products"]["recommend"].append(web_data.text.strip())

    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    
    if isinstance(web_data, bs4.element.ResultSet):
        for result_set_data in web_data:
            if result_set_data.text.strip():
                result_dict["finding-products"]["recommend"].append(result_set_data.text.strip())
    else:
        result_dict["finding-products"]["recommend"].append(web_data.text.strip())
    
    return result_dict
