import socket
import logging
from logic.MenuOptionHandler import MenuOptionHandler
import json
import select
import sys
import errno


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

    def __init__(self, host, port=3001, numToListenTo=5, timeout=0):
        super().__init__()
        self.host = host
        self.port = port
        #self.timeout = timeout
        self.numToListenTo = numToListenTo
        self.host = socket.gethostbyname(socket.gethostname())
        self.activeSocketConnections = {}
        self.entries = [sys.stdin]

    def acceptConnections(self):
        """Method that opens server for client requests"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            try:
                serverSocket.bind((self.host, self.port))
            except OSError as e:
                serverSocket.bind((self.host, self.port + 1))
            serverSocket.listen(self.numToListenTo)
            serverSocket.setblocking(0);

            # Making server able to read data from server socket and from stdin
            self.entries.append(serverSocket)

            while True:
                logging.info(
                    f"Server is waiting for client connection... <ServerConnector.py>")
                #serverSocket.settimeout(self.timeout)
                print("\n", self.entries, "\n")

                """
                If there is no input to read, select call will be blocking
                The moment it receives a connection request or something from 
                stdin (or both) code continues
                
                """
                # Will ignore write entries and exceptions for now
                entriesToRead, entriesToWrite, exceptions = None, None, None
                entriesToRead, entriesToWrite, exceptions = select.select(self.entries, [], []) # try catch to catch value error and remove connection from SOCKET_LIST
                

                for entry in entriesToRead:
                    if entry == serverSocket:
                        """New connection request"""
                        clientSocket, address = serverSocket.accept()
                        clientSocket.setblocking(False)
                        self.entries.append(clientSocket)
                        self.activeSocketConnections[clientSocket] = address
                    
                    elif entry == sys.stdin:
                        """Read from stdin"""
                        cmd = input()
                        if cmd == "quit":
                            if not self.activeSocketConnections:
                                logging.info("No active connections found, shutting down server")
                                serverSocket.close()
                                sys.exit(0)
                            else:
                                logging.info("There are active connections at the moment\n")
                        elif cmd == "con":
                            if not self.activeSocketConnections:
                                logging.info("There are no active connections\n")
                            for clientSock, address in self.activeSocketConnections.items():
                                logging.info(f"{clientSock} --> {address}")
                        else:
                            logging.info("This command does not exist\n")
                    else:
                        """New request from client"""
                        with entry:
                            logging.info(f"Connected by {self.activeSocketConnections[entry]}")
                            self.answerRequest(entry, self.activeSocketConnections[entry])


                #logging.info("Lost connection to client")

    def answerRequest(self, clientSocket, clientAddress):
        """Method that handles the connection to a client and message exchange"""
        # waits for menu option
        receivedObj = ""
        
        # needed to add this try/catch to make it work...
        # https://stackoverflow.com/questions/38419606/socket-error-errno-11-resource-temporarily-unavailable-appears-randomly/38526115
        try:
            receivedObj = clientSocket.recv(1024)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                pass

        if not receivedObj:
            logging.info(f"Client {self.activeSocketConnections[clientSocket]} closed connection")
            del self.activeSocketConnections[clientSocket]
            self.entries.remove(clientSocket)
            return
        # unserialize data
        messageComposer = self.MessageHandler()
        optionHandler = MenuOptionHandler(
            messageComposer.decode(receivedObj),
            clientSocket,
            clientAddress,
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
