from shopify_api.get_data_from_shopify import request_data
from database.mongodb import MongoDatabase
import pymongo
import logging
import time 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_transactions_from_scratch(transactions_collection):
    first_payload_transactions = '{transactions {\n    edges {\n      cursor\n      node {\n        id\n        createdAt\n        ... on AppSubscriptionSale {\n          billingInterval\n          shop {\n            name\n          }\n          app {\n            name\n          }\n          netAmount{\n              amount\n              currencyCode\n          }\n        }\n      }\n    }\n  }}'
    response = request_data(first_payload_transactions)
    
    transactions = response['data']['transactions']['edges']
    last_cursor = transactions[-1]['cursor']
    for transaction in transactions:
        find_transaction = transactions_collection.find_one({"cursor": transaction["cursor"]})
        if find_transaction is None:
            transactions_collection.insert_one(transaction)
    
    while True:
        payload_transactions = '{transactions(after: "' + last_cursor + '") {\n    edges {\n      cursor\n      node {\n        id\n        createdAt\n        ... on AppSubscriptionSale {\n          billingInterval\n          shop {\n            name\n          }\n          app {\n            name\n          }\n          netAmount{\n              amount\n              currencyCode\n          }\n        }\n      }\n    }\n  }}'
        response = request_data(payload_transactions)
        transactions = response['data']['transactions']['edges']

        if not len(transactions):
            break
        
        last_cursor = transactions[-1]['cursor']
        for transaction in transactions:
            find_transaction = transactions_collection.find_one({"cursor": transaction["cursor"]})
            if find_transaction is None:
                transactions_collection.insert_one(transaction)

def update_transactions(transactions_collection):
    last_transaction = transactions_collection.find_one(sort=[("createdAt", pymongo.DESCENDING)])
    last_cursor = last_transaction["cursor"]

    while True:
        payload_transactions = '{transactions(last: 20, before: "' + last_cursor + '") {\n    edges {\n      cursor\n      node {\n        id\n        createdAt\n        ... on AppSubscriptionSale {\n          billingInterval\n          shop {\n            name\n          }\n          app {\n            name\n          }\n          netAmount{\n              amount\n              currencyCode\n          }\n        }\n      }\n    }\n  }}'
        response = request_data(payload_transactions)
        transactions = response['data']['transactions']['edges']

        if not len(transactions):
            logging.info("No new transactions found, sleeping for 1 hour..")
            time.sleep(3600)
        
        logging.info("Found new transactions, updating..")
        last_cursor = transactions[0]['cursor']
        for transaction in transactions:
            find_transaction = transactions_collection.find_one({"cursor": transaction["cursor"]})
            if find_transaction is None:
                transactions_collection.insert_one(transaction)

        logging.info("Finished updating transactions..")

if __name__ == '__main__':
    # payload = "{\n    app (id: \"gid://partners/App/5113899\") {\n      name\n      events {\n        edges {\n          cursor\n          node {\n            type\n            occurredAt\n            shop {\n              name\n              myshopifyDomain\n            }\n          }\n        }\n      }\n    }\n  }"
    # res = request_data(payload)

    dtb = MongoDatabase()
    transactions_collection = dtb.get_transactions_collection()
    update_transactions(transactions_collection)

    
