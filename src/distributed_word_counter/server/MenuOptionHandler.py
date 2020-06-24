from distributed_word_counter.server.DatabaseHandler import DatabaseHandler

# Here the logic of word counting will happen


class MenuOptionHandler():
    def __init__(self, option, clientSocket):
        super().__init__()
        self.option = option
        self.clientSocket = clientSocket

    def manageOption(self):
        if self.option == 4:
            self.clientSocket.send(bytes("close", 'utf8'))

        elif self.option == 1:
            # list all saved files
            dbHandler = DatabaseHandler()
            files = dbHandler.getAllFiles()
            answer = ["list"]
            for f in files:
                answer.append(f"{f['name']}.{f['extension']}")
            self.clientSocket.send(bytes("\n".join(answer), 'utf8'))
            pass
        elif self.option == 2:
            # choose file to analyze
            answer = ['analize']
            pass
        elif self.option == 3:
            # create new file
            pass
