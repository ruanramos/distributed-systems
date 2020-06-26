import json
from database.DatabaseHandler import DatabaseHandler
from logic.FileAnalizer import TextAnalizer


class MessageComposer():

    def composeMessage(self, *pairs, **opts):
        message = {}
        for pair in pairs:
            message[pair[0]] = pair[1]
        for key, value in opts.items():
            if key == "encode" and value:
                return self.encodeObject(message)
        return message

    def updateMessage(self, previousMessage, *pairs, **opts):
        for pair in pairs:
            previousMessage[pair[0]] = pair[1]
        for key, value in opts.items():
            if key == "encode" and value:
                return self.encodeObject(previousMessage)
        return previousMessage

    def encodeObject(self, obj):
        return str.encode(json.dumps(obj))


class FileNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class MenuOptionHandler():
    def __init__(self, loadedData, clientSocket, clientAddress):
        super().__init__()
        self.option = int(loadedData['option'])
        self.numToAnalize = int(loadedData['numToAnalize'])
        try:
            receivedFilename, * \
                _ = loadedData['filename'].split('.')
        except (UnboundLocalError, AttributeError):
            receivedFilename = ""
        self.filenameToAnalize = receivedFilename
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.messageComposer = MessageComposer()

    def errorMessage(self, message):
        return self.messageComposer.updateMessage(
            message,
            ("filename", self.filenameToAnalize),
            ("result", "File not found")
        )

    def manageOption(self):
        if self.option == 4:
            print(
                f"Client {self.clientAddress} asked for a client side shutdown")
            self.clientSocket.send(
                self.messageComposer.composeMessage(("answer", "close"), encode=True))

        elif self.option == 1:
            # list all saved files
            print(
                f"Client {self.clientAddress} asked for a list of saved files")
            dbHandler = DatabaseHandler()
            files = dbHandler.getAllFiles()

            self.clientSocket.send(
                self.messageComposer.composeMessage(
                    ("answer", "list"),
                    ("files", [
                        f"{f['_id']} - {f['name']}.{f['extension']}" for f in files
                    ]),
                    encode=True
                )
            )
            print(
                f"Sent a list of saved files to client {self.clientAddress}")
        elif self.option == 2:
            # choose file to analyze
            message = self.messageComposer.composeMessage(
                ("answer", "analize"),
                ("result", None),
                ("filename", self.filenameToAnalize)
            )
            dbHandler = DatabaseHandler()
            # Check for the number from list
            try:
                fileToAnalize = dbHandler.getFileById(
                    int(self.filenameToAnalize))[0]
                self.messageComposer.updateMessage(
                    message,
                    ("filename",
                     f"{fileToAnalize['name']}.{fileToAnalize['extension']}")
                )
            except ValueError:
                # Check for the file name
                try:
                    fileToAnalize = dbHandler.getFile(
                        self.filenameToAnalize)[0]
                    self.messageComposer.updateMessage(
                        message, ("filename", fileToAnalize)
                    )
                except IndexError:
                    self.errorMessage(message)
                    #raise FileNotFoundError("File not found")
            except IndexError:
                self.errorMessage(message)
                #raise FileNotFoundError("File not found")
            # Got file, will analyze
            if not message["result"]:
                analizer = TextAnalizer(fileToAnalize["value"].decode())
                message["result"] = analizer.analize(self.numToAnalize)
            self.clientSocket.send(str.encode(json.dumps(message)))
            print(
                f"Sent an analysis of file {self.filenameToAnalize} to client {self.clientAddress}")
        elif self.option == 3:
            # create new file
            pass
