from distributed_word_counter.server.DatabaseHandler import DatabaseHandler


class FileAnalizer():

    def __init__(self):
        super().__init__()

    def analize(self, filename):
        # Analize logic here
        dbHandler = DatabaseHandler()
        fileToAnalize = dbHandler.getFile(filename)[0]
        fileText = fileToAnalize["value"].decode()
