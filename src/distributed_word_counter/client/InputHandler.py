from ClientScreenPrinter import ClientScreenPrinter


class InputHandler():
    """
    This class handles user input on the client side
    It's important to note that it does not make any processing besides
    getting an option and validating it.

    The processing is done at server side, with the payload received from
    the message object sent by the client.

    """

    @classmethod
    def validOption(cls, option):
        """Cheks if an option received from the user is valid"""
        try:
            return int(option) in range(1, 5)
        except ValueError:
            return False

    @classmethod
    def getOption(cls):
        """Handles logic to get user option"""
        option = input("Option: ")
        while not InputHandler.validOption(option):
            ClientScreenPrinter.invalidOption()
            ClientScreenPrinter.showMenu()
            option = input()
        return option

    @classmethod
    def handleOption(cls, option):
        """Handles option chosen by the user on client side and returns an object
        with relevant data to be sent to the server

        Parameters:
        argument1 (int): The chosen option

        Returns:
        dict:object containing the request message values

        """
        if option == "3":
            exit()
        messageObject = {
            "option": option,
            "filename": None,
            "numToAnalize": 10,
        }
        if option == "2":
            messageObject["filename"] = input(
                "What is the name of the file or number in the saved files list?\nFile: ")
            numToAnalize = input(
                "How many words? (leave blank for 10)\nNumber of Words: ")
            messageObject["numToAnalize"] = numToAnalize if numToAnalize.isnumeric(
            ) else 10

        return messageObject
