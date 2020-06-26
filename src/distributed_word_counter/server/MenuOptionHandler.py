import json
from distributed_word_counter.server.DatabaseHandler import DatabaseHandler
from distributed_word_counter.server.FileAnalizer import TextAnalizer


class MenuOptionHandler():
    def __init__(self, loadedData, clientSocket, clientAddress):
        super().__init__()
        self.option = int(loadedData['option'])
        self.numToAnalize = int(loadedData['numToAnalize'])
        if loadedData['filename']:
            receivedFilename, * \
                fileExtension = loadedData['filename'].split('.')
        self.filenameToAnalize = receivedFilename
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
                "files": [f"{f['_id']} - {f['name']}.{f['extension']}" for f in files],
            }
            self.clientSocket.send(str.encode(json.dumps(obj)))
            print(
                f"Sent a list of saved files to client {self.clientAddress}")
        elif self.option == 2:
            # choose file to analyze
            obj = {
                "answer": "analize",
                "result": None,
                "filename": self.filenameToAnalize,
            }
            dbHandler = DatabaseHandler()
            # Check for the number from list
            try:
                fileToAnalize = dbHandler.getFileById(
                    int(self.filenameToAnalize))[0]
                print(fileToAnalize)
                obj["filename"] = fileToAnalize["name"] + \
                    fileToAnalize["extension"]
            except ValueError:
                # Check for the file name
                try:
                    fileToAnalize = dbHandler.getFile(
                        self.filenameToAnalize)[0]
                    obj["filename"] = fileToAnalize
                except IndexError:
                    obj["result"] = "File not found"
                    obj["filename"] = self.filenameToAnalize
            except IndexError:
                obj["result"] = "File not found"
                obj["filename"] = self.filenameToAnalize

            if not obj["result"]:
                analizer = TextAnalizer(fileToAnalize["value"].decode())
                obj["result"] = analizer.analize(self.numToAnalize)
            self.clientSocket.send(str.encode(json.dumps(obj)))
            print(
                f"Sent an analise of file {self.filenameToAnalize} to client {self.clientAddress}")
        elif self.option == 3:
            # create new file
            pass
