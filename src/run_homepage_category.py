from crawlers import *
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from networks.proxy_management import ProxyPool
import unicodedata
import multiprocessing
from multiprocessing import Queue
import logging
from threading import Thread
import time
import random
import copy
import os
import redis
from datetime import datetime
from networks.clone_proxies import crawl_proxies_1, crawl_proxies_2, crawl_proxies_3
from database.mongodb import MongoDatabase
from utilities.utils import save_json

def check_containing_cjk_character(text):
    for character in text:
        name = unicodedata.name(character)
        if "CJK UNIFIED" in name \
            or "HIRAGANA" in name \
            or "KATAKANA" in name:
            return True
    return False

def filter_string_uppercase_or_space(text):
    return ''.join([c for c in text if c.isupper() or c == ' ' or check_containing_cjk_character(c)])

def worker_general(queue, func, identity, attempt, output_path, id_part):
    identity = identity.replace("category-", "")
    proxy_pool = ProxyPool(id_part=id_part, num_of_part=3)

    try:
        # Your code that might raise an exception goes here
        logging.info(f"Crawling {identity}, attempt {attempt}")
        crawl_result = func(proxy_pool)
        save_json(output_path, crawl_result)
        queue.put((identity, crawl_result))
        logging.info(f"Worker {identity} completed successfully")
    except Exception as e:
        if attempt < 3:
            logging.warn(f"Worker {identity} raised an exception: {e}. Retrying...")
            worker_general(queue, func, identity, attempt + 1, output_path, id_part)
        else:
            logging.warn(f"Worker {identity} raised an exception: {e}. Giving up after 3 attempts.")

            result = []
            queue.put((identity, result))

def crawl_batch_category(thread_parameter_list, category_dict):
    for i in range(len(thread_parameter_list)):
        thread_parameter = thread_parameter_list[i]
        t = Thread(target=worker_general, args=thread_parameter)
        t.start()

    queue = thread_parameter_list[0][0]
    num_of_input = 0
    while True:
        if not queue.empty():
            identity, crawl_result = queue.get()
            category_dict[identity] = crawl_result
            num_of_input += 1

        if num_of_input == len(thread_parameter_list):
            break

def main_categories(present_day):
    queue = Queue()
    category_dict = {}

    thread_parameter_list = [
        (queue, crawl_category_finding_products,'category_finding_products', 1, f'data/{present_day}/category_finding_products.json', 0),
        (queue, crawl_category_store_design, 'category_store_design', 1, f'data/{present_day}/category_store_design.json', 1),
        (queue, crawl_category_selling_products, 'category_selling_products', 1, f'data/{present_day}/category_selling_products.json', 2),
    ]

    crawl_batch_category(thread_parameter_list, category_dict)

    thread_parameter_list = [
        (queue, crawl_category_orders_and_shipping, 'category_orders_and_shipping', 1, f'data/{present_day}/category_orders_and_shipping.json', 0),
        (queue, crawl_category_marketing_and_conversion, 'category_marketing_and_conversion', 1, f'data/{present_day}/category_marketing_and_conversion.json', 1),
        (queue, crawl_category_store_management, 'category_store_management', 1, f'data/{present_day}/category_store_management.json', 2),
    ]
    crawl_batch_category(thread_parameter_list, category_dict)
    
    return category_dict

def update_proxy():
    try:
        merged_dict = crawl_proxies_1()
    except Exception as e:
        logging.warn(f"Worker crawl_proxies_1 raised an exception: {e}. Retrying...")
        merged_dict = {}
    
    try:
        merged_dict.update(crawl_proxies_2())
        get_max = 100
    except Exception as e:
        logging.warn(f"Worker crawl_proxies_2 raised an exception: {e}. Retrying...")
        get_max = 300
    merged_dict.update(crawl_proxies_3(get_max=get_max))

    save_json("src/networks/assets/list_proxy.json", merged_dict)

def main():
    mongodtb = MongoDatabase()
    tracking_collection = mongodtb.get_tracking_collection()
    # Connect to Redis server
    redis_sv = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        current_time = datetime.now()
        logging.info('Sleeping...')
        present_day = str(datetime.now().strftime("%d%m%Y"))
        if current_time.hour >= 1 and not os.path.exists(f'data/{present_day}'):
            update_proxy()
            logging.info("Finish updating proxy")

            redis_sv.set('categories_running', 1)
            
            os.makedirs(f'data/{present_day}')

            # Crawling homepage & category
            home_page_dict = crawl_apps_in_home_page()
            category_dict = main_categories(present_day)

            tracking_collection.insert_one({
                "date": present_day,    
                "category": category_dict,
                "home_page_dict": home_page_dict
                }
            )

            redis_sv.set('previous_homepage', redis_sv.get('current_homepage'))
            redis_sv.set('previous_categories', redis_sv.get('current_categories'))

            redis_sv.set('current_homepage', json.dumps(home_page_dict))
            redis_sv.set('current_categories', json.dumps(category_dict))
            
            redis_sv.set('categories_running', 0)

        time.sleep(600)

if __name__ == '__main__':
    main()