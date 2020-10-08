import socket
import sys
import json
from ClientScreenPrinter import ClientScreenPrinter
from InputHandler import InputHandler


class ClientConnector():
    """
    This class makes the connection of the client to the server

    The client message is sent as an object {option, filename, numberOfWordsToAnalyze}

    The server message is received as an object {answer, result, filename}, with some
    optional fields

    """

    @classmethod
    def tryConnection(cls):
        """Client try to start a connection"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            HOST = socket.gethostbyname(socket.gethostname())
            PORT = int(sys.argv[1])
            clientSocket.connect((HOST, PORT))
            ClientScreenPrinter.confirmConnected(HOST, PORT)
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
            try:
                ClientScreenPrinter.menu()
                requestMessage = InputHandler.handleOption(
                    InputHandler.getOption())
                encodedRequestMessage = str.encode(json.dumps(requestMessage))
                clientSocket.send(encodedRequestMessage)

                # object can be big depending on number of words!
                receivedObj = clientSocket.recv(50000)
                if not receivedObj:
                    ClientScreenPrinter.handleError()
                    raise Exception("Lost connection to server. Shutting down")

                else:
                    loadedData = json.loads(receivedObj)

                    ClientScreenPrinter.handleServerAnswer(loadedData, requestMessage['numToAnalize'])
            except Exception as e:
                exit(0)
