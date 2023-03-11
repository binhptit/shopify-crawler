from crawlers import *
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from networks.proxy_management import ProxyPool
import unicodedata
import datetime
import multiprocessing
from multiprocessing import Queue
import logging
from threading import Thread
import time
import random
import copy
import os
import redis
from database.mongodb import MongoDatabase
from utilities.utils import save_string_json, extract_key_values, filter_uncasual_slug

def worker_crawl_app_info(queue, func, identifier, attempt, id_part, num_of_part):
    proxy_pool = ProxyPool(id_part=id_part, num_of_part=num_of_part)
    try:
        crawl_result = func(identifier, proxy_pool)
        queue.put((identifier, crawl_result))
        logging.info(f"Worker APP: {identifier} completed successfully.")
    except Exception as e:
        if attempt < 3:
            logging.warn(f"Worker {identifier} raised an exception: {e}. Retrying...")
            worker_crawl_app_info(queue, func, identifier, attempt + 1, id_part, num_of_part)
        else:
            logging.warn(f"Worker {identifier} raised an exception: {e}. Giving up after 3 attempts.")

            result = {}
            queue.put((identifier, result))

def multi_thread_crawl_app_info(app_slugs, batch_size=50):
    app_dict = dict()
    app_list = list(copy.deepcopy(app_slugs))
    
    while True:
        time.sleep(random.randint(1, 4))
        if len(app_list) == 0:
            break

        if len(app_list) < batch_size:
            batch_size = len(app_list)

        app_list_batch = app_list[:batch_size]
        app_list = app_list[batch_size:]
        
        queue = Queue()
        for i in range(len(app_list_batch)):
            app_slug = app_list_batch[i]
            t = Thread(target=worker_crawl_app_info, args=(queue, crawl_informaion_app_reviews, app_slug, 1, i, batch_size))
            t.start()

        num_of_input = 0
        while True:
            if not queue.empty():
                identifier, crawl_result = queue.get()
                app_dict[identifier] = crawl_result
                num_of_input += 1

            if num_of_input == len(app_list_batch):
                break
    
    return app_dict

def main():
    ALL_CATEGORIES = [
        'category_finding_products',
        'category_store_design',
        'category_selling_products',
        'category_orders_and_shipping',
        'category_marketing_and_conversion',
        'category_store_management'
    ]
    mongodtb = MongoDatabase()
    applications_collection = mongodtb.get_applications_collection()
    tracking_collection = mongodtb.get_tracking_collection()

    redis_sv = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        logging.info("Waiting for homepage, category crawling..")
        present_day = str(datetime.datetime.now().strftime("%d%m%Y"))
        try:
            is_categories_running = int(redis_sv.get('categories_running').decode('utf-8'))
        except:
            is_categories_running = 1
        
        if os.path.exists(f"data/{present_day}"):
            if os.path.exists(f'data/{present_day}/category_store_management.json'):
                if not os.path.exists(f"data/{present_day}/applications.json"):
                    if not is_categories_running:
                        # redis_sv.delete('app_queue')
                        slugs = []
                        slug_to_short_desc_dict = {}
                        for category in ALL_CATEGORIES:
                            with open(f'data/{present_day}/{category}.json') as f:
                                category_dict = json.load(f)
                                for slug_dict in extract_key_values(category_dict, 'slug'):
                                    slugs.extend([slug for slug in slug_dict.keys() if not filter_uncasual_slug(slug)])
                                    slug_to_short_desc_dict.update(slug_dict)
                                # slugs.extend([slug_dict for slug_dict in extract_key_values(category_dict, 'slug') if not filter_uncasual_slug(list(slug_dict.keys())[0])])

                        slugs = list(set(slugs))
                        print(f"Number of slugs: {len(slugs)}")

                        app_dict_list = []

                        crawling_app_time = time.time()
                        for slug_app in slugs:
                            time.sleep(random.randint(1, 4))
                            try:
                                app_in_dtb = applications_collection.find_one({"slug": slug_app})
                                if app_in_dtb['last_updated'] == present_day:
                                    logging.info("App: " + slug_app + " already crawled today.")
                                    continue

                                proxy_pool = ProxyPool(id_part=random.randint(0,99), num_of_part=100)
                                logging.info("Crawling app: " + slug_app)
                                app_dict = crawl_information_app(slug_app, proxy_pool)
                                app_dict['slug'] = slug_app
                                app_dict['last_updated'] = present_day
                                app_dict['short_description'] = slug_to_short_desc_dict[slug_app]

                                # Push finished app to redis
                                redis_sv.lpush('app_queue', slug_app)
                                if app_in_dtb is None:
                                    applications_collection.insert_one(app_dict)
                                else:
                                    applications_collection.update_one({"slug": slug_app}, {"$set": app_dict})
                            except Exception as e:
                                logging.info(f"{e} while crawling: {slug_app}")
                                continue

                            app_dict_list.append(app_dict)

                        logging.info(f"Crawling {len(app_dict_list)} apps took {time.time() - crawling_app_time} seconds.")
                        save_string_json(f'data/{present_day}/applications.json', app_dict_list)
                        # tracking_collection.update_one({"date": present_day}, {
                        #     "$set": {"apps": app_dict_list}
                        # })
        time.sleep(1500)

if __name__ == '__main__':
    main()