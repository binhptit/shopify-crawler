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
def crawl_category_store_management(proxy_pool):
    page = urllib.request.urlopen(link_dict["categories"]["store-management"])
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "store-management": {
            "recommend": [],
        },
        "subcategory":{
            "support": subcategory_crawler("support", proxy_pool),
            "analytics": template_crawl_grid_apps(link_dict['subcategories']['analytics']['url'], proxy_pool),
            "privacy-and-security": template_crawl_grid_apps(link_dict['subcategories']['privacy-and-security']['url'], proxy_pool),
            "customer-accounts": template_crawl_grid_apps(link_dict['subcategories']['customer-accounts']['url'], proxy_pool),
            "operations": template_crawl_grid_apps(link_dict['subcategories']['operations']['url'], proxy_pool),
            "store-data": template_crawl_grid_apps(link_dict['subcategories']['store-data']['url'], proxy_pool),
            "finances": template_crawl_grid_apps(link_dict['subcategories']['finances']['url'], proxy_pool)
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["store-management"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["store-management"]["recommend"] += result_from_soup

    return result_dict
