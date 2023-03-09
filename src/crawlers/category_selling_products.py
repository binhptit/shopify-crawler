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
def crawl_category_selling_products(proxy_pool):
    page = urllib.request.urlopen(link_dict["categories"]["selling-products"])
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "selling-products": {
            "recommend": [],
        },
        "subcategory":{
            "selling-methods": subcategory_crawler("selling-methods", proxy_pool),
            "purchase-options": template_crawl_grid_apps(link_dict['subcategories']['purchase-options']['url'], proxy_pool),
            "product-variants": template_crawl_grid_apps(link_dict['subcategories']['product-variants']['url'], proxy_pool),
            "pricing": template_crawl_grid_apps(link_dict['subcategories']['pricing']['url'], proxy_pool),
            "digital-products": template_crawl_grid_apps(link_dict['subcategories']['digital-products']['url'], proxy_pool),
            "product-display": template_crawl_grid_apps(link_dict['subcategories']['product-display']['url'], proxy_pool),
            "gifts": template_crawl_grid_apps(link_dict['subcategories']['gifts']['url'], proxy_pool),
            "blockchain": template_crawl_grid_apps(link_dict['subcategories']['blockchain']['url'], proxy_pool),
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["selling-products"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["selling-products"]["recommend"] += result_from_soup

    return result_dict
