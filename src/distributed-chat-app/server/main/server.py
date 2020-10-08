import select
import socket
import sys
import threading

from application.ApplicationContext import ApplicationContext
from processing.ServerStub import ServerStub

from utils.constants import DEFAULT_SERVER_PORT, DEFAULT_HOST, NUMBER_OF_CLIENTS


class Server:
    # Server able to read commands from stdin
    port = DEFAULT_SERVER_PORT
    host = DEFAULT_HOST
    entries = [sys.stdin]
    clientThreads = []
    appContext = ApplicationContext()
    serverStub = None

    @classmethod
    def initialize_server(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((cls.host, cls.port))
            serverSocket.listen(NUMBER_OF_CLIENTS)
            serverSocket.setblocking(False)
            cls.serverStub = ServerStub(serverSocket)
            print(f"(INFO) Server listening to port {cls.port}")

            # Able to read data from requests
            cls.entries.append(serverSocket)
            while True:
                print(
                    f"(INFO) Server is waiting for requests...\n(DEBUG) Entries: {len(cls.entries)}\n(DEBUG) Active Threads: {len(cls.clientThreads)}\n")

                """
                If there is no input to read, select call will be blocking
                The moment it receives a connection request or something from 
                stdin (or both) code continues

                """
                # Will ignore write entries and exceptions for now
                entries_to_read, entries_to_write, exceptions = select.select(cls.entries, [], [])
                cls.appContext = ApplicationContext()

                for entry in entries_to_read:
                    if entry == serverSocket:
                        """New connection request"""
                        client_socket: socket
                        client_socket, address = serverSocket.accept()
                        client_socket.setblocking(False)
                        print(f"(INFO) Received connection request from {client_socket.getpeername()} and created a "
                              f"thread for it")
                        client_thread = threading.Thread(target=cls.answer_request, args=[client_socket, address])
                        client_thread.start()
                        cls.clientThreads.append(client_thread)

                    elif entry == sys.stdin:
                        """Read from stdin"""
                        cmd = input()
                        # OPTIONAL Create a commands object for scalability like {"quit":quit_function}
                        if cmd == "quit":
                            print("(INFO) Waiting for connections to be closed. No new connections allowed.")
                            for client in cls.clientThreads:
                                client.join()
                            print("(INFO) Shutting down server")
                            serverSocket.close()
                            sys.exit(0)
                        elif cmd == "con":
                            if not cls.clientThreads:
                                print("(INFO) There are no active connections\n")
                            for client_thread in cls.clientThreads:
                                # TODO add the client info to this log
                                print(f"{client_thread} --> address")
                        elif cmd == "help":
                            print("\ncon: show active socket connections\nquit: stop server")
                        else:
                            print("(ERROR) This command does not exist\n")

    @classmethod
    def answer_request(cls, client_socket, client_address):
        """Method that handles the connection to a client and message exchange"""
        while True:
            # waits for requests
            received_obj = ""
            print(f"Server thread waiting for message from {client_address}")
            a = cls.serverStub.receiveMessage(2048, client_socket)
            try:
                received_obj = cls.serverStub.decode(a)
            except Exception as e:
                pass
            if not received_obj:
                print(f"(INFO) Client {str(client_address)} closed connection")
                return

            print(f"(INFO) Client {str(client_address)} just made a request")
            print(f"(DEBUG) Received this object: {received_obj}")
