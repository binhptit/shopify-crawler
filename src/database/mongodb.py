import pymongo

class MongoDatabase:
    def __init__(self, client : str = 'mongodb://localhost:27017/'):
        self.client = pymongo.MongoClient(client)
        self.db = self.client['shopify-crawler-database']
        self.applications_collection = self.db['applications-collection']
        self.comments_collection = self.db['comments-collection']
        self.tracking_collection = self.db['trackings-collection']
    
    def get_comments_collection(self):
        return self.comments_collection

    def get_applications_collection(self):
        return self.applications_collection
    
    def get_tracking_collection(self):
        return self.tracking_collection
