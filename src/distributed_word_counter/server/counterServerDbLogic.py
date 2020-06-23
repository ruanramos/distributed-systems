from pymongo import MongoClient


def getFile(filename):
    return texts.find_one({"name": filename})


def getAllFiles():
    return texts.find()


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.test_db
    texts = db.texts

    print(getFile("test1"))
