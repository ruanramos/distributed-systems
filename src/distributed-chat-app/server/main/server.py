import errno
import json
import logging
import select
import socket
import sys
import threading
import socket
from threading import Lock
from typing import List, Any

from utils.constants import DEFAULT_SERVER_PORT, DEFAULT_HOST, NUMBER_OF_CLIENTS


# OPTIONAL: Create a logger or use better the loggin library

class Server:
    # Server able to read commands from stdin
    port: int = DEFAULT_SERVER_PORT
    host: str = DEFAULT_HOST
    entries = [sys.stdin]
    lock = threading.Lock()
    clientThreads = []

    @classmethod
    def initialize_server(cls):
        # IMPORTANT FIX THIS CLS PRECEEDING EVERYTHING
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((cls.host, cls.port))
            serverSocket.listen(NUMBER_OF_CLIENTS)
            serverSocket.setblocking(False)
            logging.info(f"(INFO) Server listening to port {cls.port}")

            # Able to read data from requests
            cls.entries.append(serverSocket)
            while True:
                logging.info(
                    f"(INFO) Server is waiting for requests...\n(DEBUG) Entries: {len(cls.entries)}\n(DEBUG) Active Sockets: {len(cls.clientThreads)}\n")

                """
                If there is no input to read, select call will be blocking
                The moment it receives a connection request or something from 
                stdin (or both) code continues

                """
                # Will ignore write entries and exceptions for now
                entries_to_read, entries_to_write, exceptions = select.select(cls.entries, [], [])

                for entry in entries_to_read:
                    if entry == serverSocket:
                        """New connection request"""
                        client_socket: socket
                        client_socket, address = serverSocket.accept()
                        client_socket.setblocking(False)
                        logging.info(f"(INFO) Received connection request from {client_socket.getpeername()}")
                        client_thread = threading.Thread(target=cls.answer_request, args=(client_socket, address))
                        client_thread.start()
                        cls.clientThreads.append(client_thread)

                    elif entry == sys.stdin:
                        """Read from stdin"""
                        cmd = input()
                        # OPTIONAL Create a commands object for scalability like {"quit":quit_function}
                        if cmd == "quit":
                            logging.info("(INFO) Waiting for connections to be closed. No new connections allowed.")
                            for client in cls.clientThreads:
                                client.join()
                            logging.info("(INFO) Shutting down server")
                            serverSocket.close()
                            sys.exit(0)
                        elif cmd == "con":
                            if not cls.clientThreads:
                                logging.info("(INFO) There are no active connections\n")
                            for client_thread in cls.clientThreads:
                                # TODO add the client info to this log
                                logging.info(f"{client_thread} --> address")
                        elif cmd == "help":
                            # OPTIONAL Fix when creating the object
                            logging.info("\ncon: show active socket connections\nquit: stop server")
                        else:
                            logging.info("(ERROR) This command does not exist\n")
                        # self.answerRequest(entry, self.activeSocketConnections[entry])

                # logging.info("Lost connection to client")

    @classmethod
    def answer_request(cls, client_socket, client_address):
        """Method that handles the connection to a client and message exchange"""

        while True:
            # waits for menu option
            received_obj = ""
            # needed to add this try/catch to make it work...
            # https://stackoverflow.com/questions/38419606/socket-error-errno-11-resource-temporarily-unavailable-appears-randomly/38526115
            try:
                received_obj = client_socket.recv(1024)
            except IOError as e:
                if e.errno == errno.EWOULDBLOCK:
                    pass

            if not received_obj:
                logging.info(f"(INFO) Client {str(client_address)} closed connection")
                return

            logging.info(f"(INFO) Client {str(client_address)} just made a request")

            # # unserialize data
            # message_composer = cls.MessageHandler()
            # option_handler = MenuOptionHandler(
            #     message_composer.decode(received_obj),
            #     client_socket,
            #     client_address,
            #     message_composer,
            # )
            # option_handler.manageOption()

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

        def update_message(self, previous_message, *pairs, **opts):
            """Updates a previous existing message object"""
            for pair in pairs:
                previous_message[pair[0]] = pair[1]
            for key, value in opts.items():
                if key == "encode" and value:
                    return self.encode(previous_message)
            return previous_message

        def encode(self, obj: object) -> bytes:
            """Encode object to be sent to client"""
            return str.encode(json.dumps(obj))

        def decode(self, obj: object) -> Any:
            """Decode object received from server"""
            return json.loads(obj)

        def send_message(self, message: bytes, client_socket: socket) -> object:
            """Send an encoded message to client"""
            client_socket.sendall(message)
