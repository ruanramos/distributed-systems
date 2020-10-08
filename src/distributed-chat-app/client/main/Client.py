from application.UserInteraction import UserInteraction

from processing.ClientContext import ClientContext
from processing.ClientStub import ClientStub

from utils.constants import *
import socket


class Client:
    """
    Client class holds host and port statically
    Instances of clients get have a socket and a user when
    username is given
    """
    host = "localhost"
    port = DEFAULT_SERVER_PORT

    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            try:
                self.reachServer(clientSocket)
            except ConnectionRefusedError as e:
                UserInteraction.handleError(error=e)
                UserInteraction.handleExit()

            # Connected to server
            user = UserInteraction.menu()

            # Generate a client context for application and data layers communication and stub
            self.context = ClientContext(self, clientSocket, user)
            self.clientStub = ClientStub(clientSocket)

            # Notify server that this client is ready to chat
            self.clientStub.subscription(ON)

            # Waits for server publishing
            self.clientStub.wait()

            # self.makeRequests(clientSocket)

    @staticmethod
    def reachServer(client_socket):
        client_socket.connect((Client.host, Client.port))

    @staticmethod
    def makeRequests(client_socket):
        while True:
            msg = input("Digite uma mensagem ('fim' para terminar):")
            if msg == 'quit':
                break

            # envia a mensagem do usuario para o servidor
            client_socket.sendAll(msg.encode('utf-8'))

            # espera a resposta do servidor
            msg = client_socket.recv(1024)

            # imprime a mensagem recebida
            print(str(msg, encoding='utf-8'))
