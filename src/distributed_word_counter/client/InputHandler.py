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
        # Cheks if an option received from the user is valid
        try:
            return int(option) in range(1, 5)
        except ValueError:
            return False

    @classmethod
    def getOption(cls):
        # Handles logic to get user option
        option = input("Option: ")
        while not InputHandler.validOption(option):
            print("Invalid option. Please choose a valid option")
            ClientScreenPrinter.showMenu()
            option = input()
        return option
