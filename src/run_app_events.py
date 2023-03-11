from shopify_api.get_data_from_shopify import request_data
from database.mongodb import MongoDatabase
import pymongo
import logging
import time 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_app_events_from_scratch(app_events_collection):
    first_app_events_payload = '{app(id: "gid://partners/App/5113899") {\n    name\n    events {\n      edges {\n        cursor\n        node {\n          type\n          occurredAt\n          shop {\n            name\n            myshopifyDomain\n          }\n        }\n      }\n    }\n  }}'
    response = request_data(first_app_events_payload)

    app_events = response['data']['app']['events']['edges']
    last_cursor = app_events[-1]['cursor']
    for app_event in app_events:
        find_app_event = app_events_collection.find_one({"cursor": app_event["cursor"]})
        if find_app_event is None:
            app_events_collection.insert_one(app_event)

    while True:
        app_events_payload = '{app(id: "gid://partners/App/5113899") {\n    name\n    events(after: "' + last_cursor + '") {\n      edges {\n        cursor\n        node {\n          type\n          occurredAt\n          shop {\n            name\n            myshopifyDomain\n          }\n        }\n      }\n    }\n  }}'
        response = request_data(app_events_payload)
        app_events = response['data']['app']['events']['edges']

        if not len(app_events):
            break
        
        last_cursor = app_events[-1]['cursor']
        for app_event in app_events:
            find_app_event = app_events_collection.find_one({"cursor": app_event["cursor"]})
            if find_app_event is None:
                app_events_collection.insert_one(app_event)

def update_app_events(app_events_collection):
    last_app_event = app_events_collection.find_one(sort=[("createdAt", pymongo.DESCENDING)])
    last_cursor = last_app_event["cursor"]

    while True:
        app_events_payload = '{app(id: "gid://partners/App/5113899") {\n    name\n    events(last: 20, before: "' + last_cursor + '") {\n      edges {\n        cursor\n        node {\n          type\n          occurredAt\n          shop {\n            name\n            myshopifyDomain\n          }\n        }\n      }\n    }\n  }}'
        response = request_data(app_events_payload)
        app_events = response['data']['app']['events']['edges']

        if not len(app_events):
            logging.info("No new app events found, sleeping for 1 hour..")
            time.sleep(3600)
        
        logging.info("Found new app events, updating..")
        last_cursor = app_events[0]['cursor']
        for app_event in app_events:
            find_app_event = app_events_collection.find_one({"cursor": app_event["cursor"]})
            if find_app_event is None:
                app_events_collection.insert_one(app_event)

if __name__ == '__main__':
    # payload = "{\n    app (id: \"gid://partners/App/5113899\") {\n      name\n      events {\n        edges {\n          cursor\n          node {\n            type\n            occurredAt\n            shop {\n              name\n              myshopifyDomain\n            }\n          }\n        }\n      }\n    }\n  }"
    # res = request_data(payload)

    dtb = MongoDatabase()
    app_events_collection = dtb.get_app_events_collection()

    # get_app_events_from_scratch(app_events_collection)
    update_app_events(app_events_collection)

    
