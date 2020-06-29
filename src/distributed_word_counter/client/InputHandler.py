from ClientScreenPrinter import ClientScreenPrinter


class InputHandler():

    @classmethod
    def validOption(cls, option):
        try:
            return int(option) in range(1, 5)
        except ValueError:
            return False

    @classmethod
    def getOption(cls):
        option = input("Option: ")
        while not InputHandler.validOption(option):
            print("Invalid option. Please choose a valid option")
            ClientScreenPrinter.showMenu()
            option = input()
        return option
