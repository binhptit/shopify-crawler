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
from utilities.utils import save_json

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
    mongodtb = MongoDatabase()
    comments_collection = mongodtb.get_comments_collection()
    present_day = str(datetime.datetime.now().strftime("%d%m%Y"))

    redis_sv = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        logging.info("Listening to Redis App Queue..")

        while redis_sv.llen('app_queue'):
            app_slug = redis_sv.rpop('app_queue')
            if app_slug is None:
                continue
            else:
                app_slug = app_slug.decode('utf-8')
                
            reviews_dict = {}
            if app_slug is not None:
                reviews_dict["slug"] = app_slug
                reviews_dict["last_updated"] = present_day

                reviews_in_dtb = comments_collection.find_one({"slug": app_slug})

                try:
                    if reviews_in_dtb is None:
                        print(f"Not found in dtb. Start crawling {app_slug}...")
                        reviews_dict["reviews"] = crawl_informaion_app_reviews(app_slug, ProxyPool(), [])
                        comments_collection.insert_one(reviews_dict)
                    else:
                        old_reviews = reviews_in_dtb["reviews"][:min(len(reviews_in_dtb["reviews"]), 10)]
                        new_reviews = crawl_informaion_app_reviews(app_slug, ProxyPool(), old_reviews)
                        reviews_dict["reviews"] = old_reviews + new_reviews

                        print(f"Found in dtb. Old reviews: {len(old_reviews)}, new reviews: {len(new_reviews)}")

                        comments_collection.update_one({"slug": app_slug}, {"$set": reviews_dict})
                except Exception as e:
                    logging.warn(f"Worker {app_slug} raised an exception: {e}. Adding back to queue...")
                    redis_sv.lpush('app_queue', app_slug)

        time.sleep(300)
        
if __name__ == '__main__':
    main()