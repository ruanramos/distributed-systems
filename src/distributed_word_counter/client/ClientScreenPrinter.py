import logging


class ClientScreenPrinter():
    """This class handles all the message printed to the console on client side"""


class ClientScreenPrinter():
    """This class handles all the message printed to the console on client side"""
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
    def invalidOption(cls):
        print("Invalid option. Please choose a valid option")

    @classmethod
    def confirmConnected(cls, host, port):
        print(f"\n\nClient connected to server!\nHost:{host}\nPort:{port}\n")

    @classmethod
    def calculateSpaces(cls, word, index, entry):
        """Makes the spaces calculations to format client screen printing"""
        spaces = [0, 0]
        spaces[0] = 4 - len(entry[0])
        spaces[1] = 10 - len(word)
        if index == 10 or index == 100 or index == 1000:
            spaces[0] -= 1
        return spaces

    @classmethod
    def printList(cls, list):
        """Print to the screen a list of files"""
        print("--------- These are the saved files --------\n")
        for i in list:
            print(i)
        print("\n--------------------------------------------\n")

    @classmethod
    def printAnalysis(cls, loadedData):
        """Print to the screen result of the analysis on client side"""
        try:
            print("\n--------------------------------------------\n")
            print(
                f"  Result of the analysis for file \"{loadedData['filename']}\": \n")
            if loadedData['result'] != "File not found":
                print(
                    f"  {obj['numToAnalize']} most used words:\n")
            for entry in loadedData["result"].items():
                word = entry[1][0].upper()
                numOfTimes = entry[1][1]
                index = int(entry[0]) + 1

                spaces = ClientScreenPrinter.calculateSpaces(
                    word, index, entry)
                print(
                    f"  {index}{spaces[0] * ' '} - \"{word}\"{spaces[1] * ' '} -->   {numOfTimes} times")
            print("\n\n--------------------------------------------")
        except AttributeError:
            print(loadedData["result"])

    @classmethod
    def handleServerAnswer(cls, loadedData):
        """Handles client console print when answer is received"""
        # this object removes the necessity of ifs and is scallable
        POSSIBLE_ANSWERS = {
            "close": lambda: logging.info("Quiting program!"),
            "list": lambda: ClientScreenPrinter.printList(loadedData["files"]),
            "analize": lambda: ClientScreenPrinter.printAnalysis(loadedData)
        }
        POSSIBLE_ANSWERS[loadedData["answer"]]()
