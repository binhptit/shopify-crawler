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
def crawl_category_marketing_and_conversion(proxy_pool):
    page = urllib.request.urlopen(link_dict["categories"]["marketing-and-conversion"])
    soup = BeautifulSoup(page, 'html.parser')
    time.sleep(random.randint(1, 3))

    result_dict = {
        "marketing-and-conversion": {
            "recommend": [],
        },
        "subcategory":{
            "email-marketing": subcategory_crawler("email-marketing", proxy_pool),
            "advertising": subcategory_crawler("advertising", proxy_pool),
            "search-engine-optimization": subcategory_crawler("search-engine-optimization", proxy_pool),
            "upselling-and-cross-selling": subcategory_crawler("upselling-and-cross-selling", proxy_pool),
            "promotions": subcategory_crawler("promotions", proxy_pool),
            "direct-marketing": template_crawl_grid_apps(link_dict['subcategories']['direct-marketing']['url'], proxy_pool),
            "cart-modification": template_crawl_grid_apps(link_dict['subcategories']['cart-modification']['url'], proxy_pool),
            "cart-recovery": template_crawl_grid_apps(link_dict['subcategories']['cart-recovery']['url'], proxy_pool),
            "content-marketing": template_crawl_grid_apps(link_dict['subcategories']['content-marketing']['url'], proxy_pool),
        }
    }

    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["marketing-and-conversion"]["recommend"] += result_from_soup
    
    web_data = soup.find('div',class_="tw-grid tw-grid-flow-dense tw-gap-gutter--mobile lg:tw-gap-gutter--desktop tw-invisible tw-transition-all tw-max-h-0 tw-duration-500 tw-ease tw-overflow-hidden tw-grid-cols-1 md:tw-grid-cols-2 xl:tw-grid-cols-3").find_all('div', class_="tw-text-heading-6 -tw-mt-xs tw-transition-colors tw-text-fg-primary group-hover:tw-text-fg-highlight-primary")
    result_from_soup : List[Dict] = get_data_from_soup(web_data)
    result_dict["marketing-and-conversion"]["recommend"] += result_from_soup

    return result_dict
