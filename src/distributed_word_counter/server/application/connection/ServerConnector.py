import socket
from logic.MenuOptionHandler import MenuOptionHandler
import json


class ServerConnector():
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((self.host, self.port))
            serverSocket.listen(self.numToListenTo)

            while True:
                print(
                    f"Server is waiting for client connection. \
                    Timeout in {self.timeout} seconds")
                serverSocket.settimeout(self.timeout)
                self.clientSocket, self.address = serverSocket.accept()
                with self.clientSocket:
                    print('Connected by', self.address)
                    self.executionLoop()
                print("Lost connection to client")

    def executionLoop(self):
        while True:
            # waits for menu option
            receivedObj = self.clientSocket.recv(1024)
            if not receivedObj:
                break
            # unserialize data
            messageComposer = self.MessageComposer()
            optionHandler = MenuOptionHandler(
                messageComposer.decodeObject(receivedObj),
                self.clientSocket,
                self.address,
                messageComposer,
            )
            optionHandler.manageOption()

    class MessageComposer():
        def composeMessage(self, *pairs, **opts):
            message = {}
            for pair in pairs:
                message[pair[0]] = pair[1]
            for key, value in opts.items():
                if key == "encode" and value:
                    return self.encodeObject(message)
            return message

        def updateMessage(self, previousMessage, *pairs, **opts):
            for pair in pairs:
                previousMessage[pair[0]] = pair[1]
            for key, value in opts.items():
                if key == "encode" and value:
                    return self.encodeObject(previousMessage)
            return previousMessage

        def encodeObject(self, obj):
            return str.encode(json.dumps(obj))

        def decodeObject(self, obj):
            return json.loads(obj)
