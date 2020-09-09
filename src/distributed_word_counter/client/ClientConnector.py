import socket
import logging
import sys
import json
from ClientScreenPrinter import ClientScreenPrinter
from InputHandler import InputHandler


class ClientConnector():
    """
    This class makes the connection of the client to the server
    The client message is sent as an object {option, filename, numberOfWordsToAnalyze}
    The server message is received as an object {answer, result, filename}
    """
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

                # object can be big depending on number of words!
                receivedObj = clientSocket.recv(50000)
                loadedData = json.loads(receivedObj)

                ClientScreenPrinter.handleServerAnswer(loadedData)
            except Exception:
                raise Exception("Lost connection to server. Shutting down")
