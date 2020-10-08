from utils.constants import MENU_OPTIONS as options
from utils.constants import MENU_TEXT as menu_text
from utils.User import User


class UserInteraction:
    """This class handles all user interaction"""

    @classmethod
    def menu(cls) -> User:
        """Shows menu and get option / chat username"""
        print(f"""
        {menu_text}

                1: {options['1']}
                2: {options['2']}
                """)

        option = cls.getOption()
        if option == '1':
            return User(cls.userLogin())
        elif option == '2':
            cls.handleExit()

    @classmethod
    def getOption(cls):
        option = input()
        while option not in options.keys():
            cls.invalidOption()
            option = input()
        return option

    @classmethod
    def userLogin(cls):
        print("Choose a nickname: ", end="")
        username = input()
        return username

    @classmethod
    def invalidOption(cls):
        print("(ERROR) Invalid option. Please choose a valid option")

    @classmethod
    def confirmConnected(cls, host, port):
        print(f"\n\n(INFO) Client connected to server!\nHost:{host}\nPort:{port}\n")

    @classmethod
    def confirmDisconnected(cls):
        print("(INFO) Client is closing connection")

    @classmethod
    def printList(cls, elements, title):
        """Print to the screen a list of elements with a title"""
        print(f"--------- {title} --------\n")
        for i in elements:
            print(i)
        print("\n--------------------------------------------\n")

    @classmethod
    def handleExit(cls):
        print("(INFO) Client is closing connection!")
        exit(0)

    @classmethod
    def handleError(cls, **error):
        if not error:
            print("(ERROR) Lost connection to server")
            exit(0)
        print(f"(ERROR) {error['error']}")

    @classmethod
    def handleServerAnswer(cls, loadedData, numToAnalize):
        """Handles client console print when answer is received"""
        # this object removes the necessity of ifs and is scallable
        POSSIBLE_ANSWERS = {
            "close": lambda: UserInteraction.handleExit(),
            "list": lambda: UserInteraction.printList(loadedData["files"]),
            "analize": lambda: UserInteraction.printAnalysis(loadedData, numToAnalize)
        }
        POSSIBLE_ANSWERS[loadedData["answer"]]()
