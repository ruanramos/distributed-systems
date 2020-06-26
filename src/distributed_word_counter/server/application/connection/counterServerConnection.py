import socket
from logic.MenuOptionHandler import MenuOptionHandler
import json

# For Server socket, always use this order
# socket()
# bind()
# listen()
# accept() -> can loop


class Connector():
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
                    while True:
                        # waits for menu option
                        receivedObj = self.clientSocket.recv(1024)
                        if not receivedObj:
                            break
                        # unserialize data
                        loadedData = json.loads(receivedObj)

                        optionHandler = MenuOptionHandler(
                            loadedData, self.clientSocket, self.address)
                        optionHandler.manageOption()
                print("Lost connection to client")

    # TODO create a method to send and receive messages, removing
    # this work from menu handler
