from distributed_word_counter.server.counterServerDbLogic import getFile, getAllFiles

# Here the logic of word counting will happen


class OptionHandler():
    def __init__(self, option):
        super().__init__()
        self.option = option

    def manageOption(self):
        if self.option == 1:
            # list all saved files
            pass
        elif self.option == 2:
            # choose file to analyze
            pass
        elif self.option == 3:
            # create new file
            pass
        else:
            # quit
            pass
