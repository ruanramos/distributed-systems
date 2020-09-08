import json
import logging
from database.DatabaseHandler import DatabaseHandler
from logic.FileAnalizer import TextAnalizer


class MenuOptionHandler():

    def __init__(self, loadedData, clientSocket,
                 clientAddress, messageComposer):
        super().__init__()
        self.option = int(loadedData['option'])
        self.numToAnalize = int(loadedData['numToAnalize'])
        try:
            receivedFilename, *_ = loadedData['filename'].split('.')
        except (UnboundLocalError, AttributeError):
            receivedFilename = ""
        self.filenameToAnalize = receivedFilename
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.messageComposer = messageComposer

    def sendErrorMessage(self, message):
        return self.messageComposer.updateMessage(
            message,
            ("filename", self.filenameToAnalize),
            ("result", "File not found")
        )

    def handleQuitOption(self):
        logging.info(
            f"Client {self.clientAddress} asked for a client side shutdown")
        self.clientSocket.send(self.messageComposer.composeMessage(
            ("answer", "close"), encode=True))

    def handleListOption(self):
        logging.info(
            f"Client {self.clientAddress} asked for a list of saved files")
        self.clientSocket.send(
            self.messageComposer.composeMessage(
                ("answer", "list"),
                ("files",
                 [f"{f['_id']} - {f['name']}.{f['extension']}" for f in DatabaseHandler().getAllFiles()]),
                encode=True
            )
        )
        logging.info(
            f"Sent a list of saved files to client {self.clientAddress}")

    def handleAnalysis(self):
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
                    message,
                    (
                        "filename",
                        f"{fileToAnalize['name']}.{fileToAnalize['extension']}"
                    )
                )
            except IndexError:
                self.sendErrorMessage(message)
        except IndexError:
            self.sendErrorMessage(message)
        # Got file, will analyze
        if not message["result"]:
            analizer = TextAnalizer(fileToAnalize["value"].decode())
            message["result"] = analizer.analize(self.numToAnalize)

        self.clientSocket.send(str.encode(json.dumps(message)))
        try:
            logging.info(
                f"Sent an analysis of file \"{fileToAnalize['name']}.{fileToAnalize['extension']}\" to client {self.clientAddress}")
        except Exception as e:
            logging.warning(
                f"{e}\nFile not found. Sent an error message to client {self.clientAddress}")

    def manageOption(self):
        if self.option == 3:
            self.handleQuitOption()
        elif self.option == 1:
            self.handleListOption()
        elif self.option == 2:
            self.handleAnalysis()
