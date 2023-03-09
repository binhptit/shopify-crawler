import urllib
from bs4 import BeautifulSoup
from .utils import read_json, get_data_from_soup, template_crawl_grid_apps, subcategory_crawler
import time
import random
from typing import List, Dict
import logging
from .decorators import time_log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
link_dict = read_json("src/crawlers/configs/link_config.json")

@time_log
def crawl_category_orders_and_shipping(proxy_pool):
    page = urllib.request.urlopen(link_dict["categories"]["orders-and-shipping"])
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "orders-and-shipping": {
            "recommend": [],
        },
        "subcategory":{
            "fulfilling-orders": subcategory_crawler("fulfilling-orders", proxy_pool),
            "managing-orders": template_crawl_grid_apps(link_dict['subcategories']['managing-orders']['url'], proxy_pool),
            "managing-inventory": template_crawl_grid_apps(link_dict['subcategories']['managing-inventory']['url'], proxy_pool),
            "delivery-and-pickups": template_crawl_grid_apps(link_dict['subcategories']['delivery-and-pickups']['url'], proxy_pool),
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["orders-and-shipping"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["orders-and-shipping"]["recommend"] += result_from_soup

    return result_dict
