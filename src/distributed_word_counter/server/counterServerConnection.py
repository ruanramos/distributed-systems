import socket

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

    def acceptConnections(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            self.host = socket.gethostbyname(socket.gethostname())
            print(self.host, socket.gethostname(),
                  socket.gethostbyname(socket.gethostname()))
            serverSocket.bind((self.host, self.port))
            serverSocket.listen(self.numToListenTo)
            print(
                f"Server is waiting for client connection. Timeout in {self.timeout} seconds")
            serverSocket.settimeout(self.timeout)
            return serverSocket.accept()
