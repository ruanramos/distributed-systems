import socket
import logging
import sys
import json
from ClientScreenPrinter import ClientScreenPrinter
from InputHandler import InputHandler


class ClientConnector():
    """This class makes the connection of the client to the server"""
    @classmethod
    def tryConnection(cls):
        """Client try to start a connection"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            HOST = socket.gethostbyname(socket.gethostname())
            PORT = int(sys.argv[1])
            clientSocket.connect((HOST, PORT))
            logging.info("\n\nClient connected to server!")
            ClientConnector.connectionLoop(clientSocket)

    @classmethod
    def connectionLoop(cls, clientSocket):
        """Create the loop that handles the connection and communication after
         connection is established

        Parameters:
        argument1 (socket): The cliente socket

        Returns:
        void

        """
        while True:
            ClientScreenPrinter.showMenu()
            try:
                # this requestMessage could be handled by a different component
                requestMessage = str.encode(
                    json.dumps(
                        InputHandler.handleOption(
                            InputHandler.getOption()
                        )
                    )
                )

                clientSocket.send(requestMessage)

                # ---- receiving response ------
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
