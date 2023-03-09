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
def crawl_category_store_design(proxy_pool):

    page = urllib.request.urlopen(link_dict["categories"]["store-design"])
    soup = BeautifulSoup(page, 'html.parser')

    result_dict = {
        "store-design": {
            "recommend": [],
        },
        "subcategory":{
            "social-proof": subcategory_crawler("social-proof", proxy_pool),
            "internationalization": subcategory_crawler("internationalization", proxy_pool),
            "store-pages": subcategory_crawler("store-pages", proxy_pool),
            "store-alerts": template_crawl_grid_apps(link_dict['subcategories']['store-alerts']['url'], proxy_pool),
            "navigation-and-search": template_crawl_grid_apps(link_dict['subcategories']['navigation-and-search']['url'], proxy_pool),
            "notifications": template_crawl_grid_apps(link_dict['subcategories']['notifications']['url'], proxy_pool),
            "images-and-media": template_crawl_grid_apps(link_dict['subcategories']['images-and-media']['url'], proxy_pool),
            "page-enhancements": template_crawl_grid_apps(link_dict['subcategories']['page-enhancements']['url'], proxy_pool),
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["store-design"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3")
    web_data = web_data.find_all('div', class_="tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-xs")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["store-design"]["recommend"] += result_from_soup

    return result_dict
