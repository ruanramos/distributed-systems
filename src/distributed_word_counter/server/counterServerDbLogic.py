from pymongo import MongoClient


class DatabaseQuerier():
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        # Database name and collection name being hardcoded for now
        self.db = self.client.test_db
        self.collection = self.db.texts

    def getFile(self, filename):
        return self.collection.find_one({"name": filename})

    def getAllFiles(self):
        return self.collection.find()
