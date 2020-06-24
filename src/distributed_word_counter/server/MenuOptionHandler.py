import distributed_word_counter.server.counterServerDbLogic as dbl

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
            dbQuerier = dbl.DatabaseQuerier()
            files = dbQuerier.getAllFiles()
            for f in files:
                print(f"{f['name']}.{f['extension']}")
            pass
        elif self.option == 2:
            # choose file to analyze
            pass
        elif self.option == 3:
            # create new file
            pass
