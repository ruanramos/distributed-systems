import socket
import logging
import sys
import json
from ClientScreenPrinter import ClientScreenPrinter
from InputHandler import InputHandler


class ClientConnector():
    @classmethod
    def tryConnection(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            HOST = socket.gethostbyname(socket.gethostname())
            PORT = int(sys.argv[1])
            clientSocket.connect((HOST, PORT))
            logging.info("\n\nClient connected to server!")
            ClientConnector.connectionLoop(clientSocket)

    @classmethod
    def connectionLoop(cls, clientSocket):
        while True:
            ClientScreenPrinter.showMenu()
            try:
                option = InputHandler.getOption()
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

                            spaces = ClientScreenPrinter.calculateSpaces(
                                word, index, entry)
                            print(
                                f"  {index}{spaces[0] * ' '} - \"{word}\"{spaces[1] * ' '} -->   {numOfTimes} times")
                        print("\n\n--------------------------------------------")
                    except AttributeError:
                        print(loadedData["result"])
            except Exception:
                raise Exception("Lost connection to server. Shutting down")
