from pymongo import MongoClient
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


class DatabaseHandler():
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        # Database name and collection name being hardcoded for now
        self.db = self.client.test_db
        self.collection = self.db.texts
        self.filesPath = "/home/ruan/Codes/distributed-systems/src/distributed_word_counter/server/files"

    def getFile(self, filename):
        return self.collection.find({"name": filename}).limit(1)

    def getFileById(self, fileId):
        return self.collection.find({"_id": fileId}).limit(1)

    def getAllFiles(self):
        return self.collection.find()

    def saveAllFiles(self):
        # Save all files from the files folder to mongodb
        # texts collection on test_db
        for i, entry in enumerate(os.scandir(self.filesPath)):
            if entry.path.endswith(".txt") and entry.is_file():
                with open(entry.path, 'r') as f:
                    fullName = f.name.split('/')[-1].split('.')
                    self.collection.insert(
                        {
                            "_id": i,
                            "name": fullName[0],
                            "extension": fullName[1],
                            "value": bytes(f.read(), 'utf8')
                        }
                    )
                    logging.info(f'Ok to file {f}')
        return


if __name__ == "__main__":
    a = DatabaseHandler()
    # for f in a.getAllFiles():
    # print(f["value"][:300])
    a.collection.drop()
    a.saveAllFiles()
