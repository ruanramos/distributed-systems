import socket
import sys
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


def showMenu():
    print("""
    You can check the files that are saved and choose one to be analyzed.
    The analysis will show you the most used words in the file.

            1- See saved files
            2- Choose a file to analize
            3- Create a new file
            4- Quit
            """)


def validOption(option):
    try:
        return int(option) in range(1, 5)
    except ValueError:
        return False


def getOption():
    option = input("Option: ")
    while not validOption(option):
        print("Invalid option. Please choose a valid option")
        showMenu()
        option = input()
    return option


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = int(sys.argv[1])
        clientSocket.connect((HOST, PORT))
        logging.info("\n\nClient connected to server!")

        while True:
            showMenu()
            try:
                option = getOption()
                obj = {
                    "option": option,
                    "filename": None,
                    "numToAnalize": 10,
                }
                if option == "2":
                    obj["filename"] = input(
                        "What is the name of the file or number in the saved files list?\nFile: ")
                    numToAnalize = input(
                        "How many words? (leave blank for 10)\nNumber of Words: ")
                    obj["numToAnalize"] = numToAnalize if numToAnalize.isnumeric() else 10
                serializedObj = json.dumps(obj)
                clientSocket.send(str.encode(serializedObj))

                # object can be big depending on number of words!
                receivedObj = clientSocket.recv(50000)
                loadedData = json.loads(receivedObj)
                if loadedData["answer"] == "close":
                    logging.info("Quiting program!")
                    exit(0)
                elif loadedData["answer"] == "list":
                    print("--------- These are the saved files --------\n")
                    for i in loadedData["files"]:
                        print(i)
                    print("\n--------------------------------------------\n")
                elif loadedData["answer"] == "analize":
                    # Show analizes info here
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
                            print(
                                f"  {index} - \"{word}\" --> {numOfTimes} times")
                        print("\n\n--------------------------------------------")
                    except AttributeError:
                        print(loadedData["result"])
            except Exception:
                raise Exception("Lost connection to server. Shutting down")

    logging.info("Client is closing connection")
