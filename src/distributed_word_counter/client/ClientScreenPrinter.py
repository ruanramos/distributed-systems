class ClientScreenPrinter():

    @classmethod
    def showMenu(cls):
        print("""
        You can check the files that are saved and choose one to be analyzed.
        The analysis will show you the most used words in the file.

                1- See saved files
                2- Choose a file to analize
                3- Quit
                """)

    @classmethod
    def calculateSpaces(cls, word, index, entry):
        # Makes the spaces calculations to format client screen printing
        spaces = [0, 0]
        spaces[0] = 4 - len(entry[0])
        spaces[1] = 10 - len(word)
        if index == 10 or index == 100 or index == 1000:
            spaces[0] -= 1
        return spaces
