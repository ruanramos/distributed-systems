from ClientScreenPrinter import ClientScreenPrinter


class InputHandler():

    def __init__(self, option):
        super().__init__()
        self.option = option

    @staticmethod
    def validOption(option):
        try:
            return int(option) in range(1, 5)
        except ValueError:
            return False

    @staticmethod
    def getOption():
        option = input("Option: ")
        while not InputHandler.validOption(option):
            print("Invalid option. Please choose a valid option")
            ClientScreenPrinter.showMenu()
            option = input()
        return InputHandler(option)

    def handleAnalysisOption(self):
        clientRequestMessage = {
            "option": self.option,
            "filename": None,
            "numToAnalize": 10,
        }
        if self.option == "2":
            clientRequestMessage["filename"] = input(
                "What is the name of the file or number in the saved files list?\nFile: ")
            numToAnalize = input(
                "How many words? (leave blank for 10)\nNumber of Words: ")
            clientRequestMessage["numToAnalize"] = numToAnalize if numToAnalize.isnumeric(
            ) else 10
        return clientRequestMessage
