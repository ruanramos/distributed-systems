import socket
import logging
import sys
import json
from ClientScreenPrinter import ClientScreenPrinter
from InputHandler import InputHandler


class ClientConnector():

    @staticmethod
    def tryConnection():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            HOST = socket.gethostbyname(socket.gethostname())
            PORT = int(sys.argv[1])
            clientSocket.connect((HOST, PORT))
            logging.info("\n\nClient connected to server!")
            ClientConnector.connectionLoop(clientSocket)

    @staticmethod
    def closeConnection():
        logging.info("Quiting program!")
        exit(0)

    @staticmethod
    def connectionLoop(clientSocket):
        while True:
            ClientScreenPrinter.showMenu()
            try:
                clientRequestMessage = (InputHandler
                                        .getOption()
                                        .handleAnalysisOption())
                clientSocket.send(str.encode(
                    json.dumps(clientRequestMessage)))
                ClientConnector.handleServerResponse(
                    clientSocket, clientRequestMessage)
            except Exception:
                raise Exception("Lost connection to server. Shutting down")

    @staticmethod
    def handleServerResponse(clientSocket, clientRequestMessage):
        serverResponseMessage = clientSocket.recv(50000)
        decodedResponse = json.loads(serverResponseMessage)

        if decodedResponse["answer"] == "close":
            ClientConnector.closeConnection()
        elif decodedResponse["answer"] == "list":
            ClientScreenPrinter.showSavedFilesList(
                decodedResponse["files"])
        elif decodedResponse["answer"] == "analize":
            try:
                ClientScreenPrinter.printAnalysisHeader(
                    decodedResponse, clientRequestMessage['numToAnalize'])
                ClientScreenPrinter.showAnalysisResult(
                    decodedResponse["result"])
            except AttributeError:
                ClientScreenPrinter.logFileNotFoundError(
                    decodedResponse["result"])
