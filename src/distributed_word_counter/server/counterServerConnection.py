import socket
from distributed_word_counter.server.counterServerLogic import OptionHandler

# For Server socket, always use this order
# socket()
# bind()
# listen()
# accept() -> can loop


class Connector():
    def __init__(self, host, port, timeout=0):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout

    def listenToClients(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            self.host = socket.gethostbyname(socket.gethostname())
            print(self.host, socket.gethostname(),
                  socket.gethostbyname(socket.gethostname()))
            serverSocket.bind((self.host, self.port))
            serverSocket.listen(1)
            print(
                f"Server is waiting for client connection. Timeout in {self.timeout} seconds")
            serverSocket.settimeout(self.timeout)
            return serverSocket.accept()
