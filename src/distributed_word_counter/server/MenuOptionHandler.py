import json
from distributed_word_counter.server.DatabaseHandler import DatabaseHandler
from distributed_word_counter.server.FileAnalizer import TextAnalizer


class MenuOptionHandler():
    def __init__(self, loadedData, clientSocket, clientAddress):
        super().__init__()
        self.option = int(loadedData['option'])
        if loadedData['filename']:
            filename, *fileExtension = loadedData['filename'].split('.')
            self.filenameToAnalize = filename
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def manageOption(self):
        if self.option == 4:
            obj = {
                "answer": "close",
            }
            print(
                f"Client {self.clientAddress} asked for a client side shutdown")
            self.clientSocket.send(str.encode(json.dumps(obj)))

        elif self.option == 1:
            # list all saved files
            print(
                f"Client {self.clientAddress} asked for a list of saved files")
            # TODO pass this part to the analizer
            dbHandler = DatabaseHandler()
            files = dbHandler.getAllFiles()
            obj = {
                "answer": "list",
                "files": [f"{f['name']}.{f['extension']}" for f in files],
            }
            self.clientSocket.send(str.encode(json.dumps(obj)))
            print(
                f"Sent a list of saved files to client {self.clientAddress}")
        elif self.option == 2:
            # choose file to analyze
            obj = {
                "answer": "analize",
                "result": None,
            }
            dbHandler = DatabaseHandler()
            fileToAnalize = dbHandler.getFile(self.filenameToAnalize)[0]
            analizer = TextAnalizer(fileToAnalize["value"].decode())
            obj["result"] = analizer.analize(20)
            self.clientSocket.send(str.encode(json.dumps(obj)))
            print(
                f"Sent an analise of file {self.filenameToAnalize} to client {self.clientAddress}")
        elif self.option == 3:
            # create new file
            pass
