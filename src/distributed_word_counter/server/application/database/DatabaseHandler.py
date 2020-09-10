from pymongo import MongoClient
import os
import logging


class DatabaseHandler():
    """This is the database layer. It receives a request call from logic layer

    I made the option to work with a NOSQL database. Files are stored in a 
    mongodb database, in the format of JSON objects.

    {
        "_id": int,
        "name": String,
        "extension": String,
        "value": bytes
    }

    The text values are encoded and saved as bytes and decoded when the objects 
    are queried.

    """

    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        # Database name and collection name being hardcoded for now
        self.db = self.client.distributed_word_counter
        self.collection = self.db.files
        self.filesPath = "/home/ruanramos/Codes/distributed-systems/src/distributed_word_counter/server/files"

    def getFile(self, filename):
        """Query db by filename"""
        return self.collection.find(
            {
                "name":
                {
                    "$regex": "^" + filename.lower() + "$", "$options": 'i'
                }
            }
        ).limit(1)

    def getFileById(self, fileId):
        """Query db by id"""
        return self.collection.find({"_id": fileId}).limit(1)

    def getAllFiles(self):
        """Query db for all files"""
        return self.collection.find()

    def saveFile(self, path):
        """Save an specified file to the database

        This method was added to make the code closer to what was 
        asked. It's not being used, but the functionality exists.

        Call this method to save a file by it's system path and the
        analysis will work just fine.

        """
        if path.endswith(".txt"):
            try:
                with open(path, 'r') as f:
                    fullName = f.name.split('/')[-1].split('.')
                    self.collection.insert(
                        {
                            "name": fullName[0],
                            "extension": fullName[1],
                            "value": bytes(f.read(), 'utf8')
                        }
                    )
                    logging.info(f'Ok to file {f}')
            except FileNotFoundError:
                raise Exception("File not found")

    def saveAllFiles(self):
        """Save all files from the server files folder to mongodb

        This method is here only to be called by the main method in this 
        class to populate the db with files

        """
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
    """Execute this main method to reset the db and load files 
    from files folder into mongodb
    """
    a = DatabaseHandler()
    # a.saveFile("/home/ruanramos/Desktop/a.txt")
    # for f in a.getAllFiles():
    #    print(f["value"][:300])
    a.collection.drop()
    a.saveAllFiles()
