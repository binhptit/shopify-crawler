import urllib
from bs4 import BeautifulSoup
from .utils import read_json, get_data_from_soup, template_crawl_grid_apps, subcategory_crawler
import time
import random
from typing import List
import logging
from .decorators import time_log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
link_dict = read_json("src/crawlers/configs/link_config.json")

@time_log
def crawl_category_store_management():
    page = urllib.request.urlopen(link_dict["categories"]["store-management"])
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "store-design": {
            "recommend": [],
        },
        "subcategory":{
            "support": subcategory_crawler("support"),
            "analytics": template_crawl_grid_apps(link_dict['subcategories']['analytics']['url']),
            "privacy-and-security": template_crawl_grid_apps(link_dict['subcategories']['privacy-and-security']['url']),
            "customer-accounts": template_crawl_grid_apps(link_dict['subcategories']['customer-accounts']['url']),
            "operations": template_crawl_grid_apps(link_dict['subcategories']['operations']['url']),
            "store-data": template_crawl_grid_apps(link_dict['subcategories']['store-data']['url']),
            "finances": template_crawl_grid_apps(link_dict['subcategories']['finances']['url'])
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[str] = get_data_from_soup(web_data)
    result_dict["store-design"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[str] = get_data_from_soup(web_data)
    result_dict["store-design"]["recommend"] += result_from_soup

    return result_dict
