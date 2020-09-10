import socket
import logging
from logic.MenuOptionHandler import MenuOptionHandler
import json


class ServerConnector():
    """This class handles all the communication for the server

    The server is iterative, it can only treat requests from
    one client at a time.

    Messages are received and sent as JSON objects, encoded
    before sending and decoded on receive.

    The client message is sent as an object {option, filename, numberOfWordsToAnalyze}

    The server message is received as an object {answer, result, filename}, with some
    optional fields

    """

    def __init__(self, host, port, numToListenTo=1, timeout=0):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.numToListenTo = numToListenTo
        self.host = socket.gethostbyname(socket.gethostname())
        self.clientSocket = None
        self.address = None

    def acceptConnections(self):
        """Method that opens server for client requests"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((self.host, self.port))
            serverSocket.listen(self.numToListenTo)

            while True:
                logging.info(
                    f"Server is waiting for client connection. Timeout in {self.timeout} seconds")
                serverSocket.settimeout(self.timeout)
                self.clientSocket, self.address = serverSocket.accept()
                with self.clientSocket:
                    logging.info(f"Connected by {self.address}")
                    self.connectionLoop()
                logging.info("Lost connection to client")

    def connectionLoop(self):
        """Method that handles the connection to a client and message exchange"""
        while True:
            # waits for menu option
            receivedObj = self.clientSocket.recv(1024)
            if not receivedObj:
                break
            # unserialize data
            messageComposer = self.MessageHandler()
            optionHandler = MenuOptionHandler(
                messageComposer.decode(receivedObj),
                self.clientSocket,
                self.address,
                messageComposer,
            )
            optionHandler.manageOption()

    class MessageHandler():
        """Class that handles messages related tasks

        It's a nested class since the concept of a message object only 
        exists in the connector context

        """

        def composeMessage(self, *pairs, **opts):
            """Compose a message given the arguments in pairs or flags"""
            message = {}
            for pair in pairs:
                message[pair[0]] = pair[1]
            for key, value in opts.items():
                if key == "encode" and value:
                    return self.encode(message)
            return message

        def updateMessage(self, previousMessage, *pairs, **opts):
            """Updates a previous existing message object"""
            for pair in pairs:
                previousMessage[pair[0]] = pair[1]
            for key, value in opts.items():
                if key == "encode" and value:
                    return self.encode(previousMessage)
            return previousMessage

        def encode(self, obj):
            """Encode object to be sent to client"""
            return str.encode(json.dumps(obj))

        def decode(self, obj):
            """Decode object received from server"""
            return json.loads(obj)

        def sendMessage(self, message, clientSocket):
            """Send an encoded message to client"""
            clientSocket.send(message)
