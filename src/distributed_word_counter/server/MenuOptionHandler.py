from distributed_word_counter.server.DatabaseHandler import DatabaseHandler
from distributed_word_counter.server.FileAnalizer import FileAnalizer

# Here the logic of word counting will happen


class MenuOptionHandler():
    def __init__(self, loadedData, clientSocket, clientAddress):
        super().__init__()
        self.option = int(loadedData['option'])
        self.fileToAnalize = loadedData['filename']
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def manageOption(self):
        if self.option == 4:
            self.clientSocket.send(bytes("close", 'utf8'))

        elif self.option == 1:
            # list all saved files
            print(
                f"Client {self.clientAddress} asked for a list of saved files")
            dbHandler = DatabaseHandler()
            files = dbHandler.getAllFiles()
            answer = ["list"]
            for f in files:
                answer.append(f"{f['name']}.{f['extension']}")
            self.clientSocket.send(bytes("\n".join(answer), 'utf8'))
            print(
                f"Sent a list of saved files to client {self.clientAddress}")
        elif self.option == 2:
            # choose file to analyze
            answer = ['analize']
            FileAnalizer()
            pass
        elif self.option == 3:
            # create new file
            pass
