from crawlers import *
import json

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    # Crawling app information
    # app_slug =  "walmart-marketplace"
    # crawl_result = crawl_information_app(app_slug)
    # save_json(f'data/{app_slug}.json', crawl_result)

    # Crawling homepage
    # crawl_result = crawl_apps_in_home_page()
    # save_json(f'data/home-page.json', crawl_result)

    # Crawling query input
    # crawl_result = crawl_searching_result('tiktok pixel alo bar')
    # save_json(f'data/search_result.json', crawl_result)

    # Crawling category finding products
    # crawl_result = crawl_category_finding_products()
    # save_json(f'data/category_finding_products.json', crawl_result)

    # Crawling category store design
    # crawl_result = crawl_category_store_design()
    # save_json(f'data/category_store_design.json', crawl_result)

    # Crawling category selling products
    # crawl_result = crawl_category_selling_products()
    # save_json(f'data/category_selling_products.json', crawl_result)

    # Crawling category orders and shipping
    # crawl_result = crawl_category_orders_and_shipping()
    # save_json(f'data/category_orders_and_shipping.json', crawl_result)

    # Crawling category marketing and conversion
    # crawl_result = crawl_category_marketing_and_conversion()
    # save_json(f'data/category_marketing_and_conversion.json', crawl_result)

    # Crawling category store management
    crawl_result = crawl_category_store_management()
    save_json(f'data/category_store_management.json', crawl_result)