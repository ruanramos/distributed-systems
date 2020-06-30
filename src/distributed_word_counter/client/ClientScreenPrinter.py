class ClientScreenPrinter():

    @staticmethod
    def showMenu():
        print("""
        You can check the files that are saved and choose one to be analyzed.
        The analysis will show you the most used words in the file.

                1- See saved files
                2- Choose a file to analize
                3- Create a new file
                4- Quit
                """)

    @staticmethod
    def calculateSpaces(word, index, entry):
        spaces = [0, 0]
        spaces[0] = 4 - len(entry[0])
        spaces[1] = 10 - len(word)
        if index == 10 or index == 100 or index == 1000:
            spaces[0] -= 1
        return spaces

    @staticmethod
    def showSavedFilesList(files):
        print("--------- These are the saved files --------\n")
        for i in files:
            print(i)
        print("\n--------------------------------------------\n")

    @staticmethod
    def printAnalysisHeader(serverResponseMessage, numToAnalize):
        print("\n--------------------------------------------\n")
        print(
            f"  Result of the analysis for file \"{serverResponseMessage['filename']}\": \n")
        if serverResponseMessage['result'] != "File not found":
            print(
                f"  {numToAnalize} most used words:\n")

    @staticmethod
    def showAnalysisResult(result):
        for entry in result.items():
            word = entry[1][0].upper()
            numOfTimes = entry[1][1]
            index = int(entry[0]) + 1
            spaces = ClientScreenPrinter.calculateSpaces(word, index, entry)
            print(
                f"  {index}{spaces[0] * ' '} - \"{word}\"{spaces[1] * ' '} -->   {numOfTimes} times")
        print("\n\n--------------------------------------------")

    @staticmethod
    def logFileNotFoundError(message):
        print(message)
