import sys
import json
from distributed_word_counter.server.counterServerConnection import Connector
from distributed_word_counter.server.MenuOptionHandler import MenuOptionHandler

if __name__ == "__main__":
    HOST = ""
    PORT = int(sys.argv[1])
    CON_TIMEOUT = 15
    LISTEN_BACKLOG = 1
    connector = Connector(HOST, PORT, LISTEN_BACKLOG, CON_TIMEOUT)
    clientSocket, address = connector.acceptConnections()

    with clientSocket:
        print('Connected by', address)
        # waits for menu option
        receivedObj = clientSocket.recv(1024)
        loadedData = json.loads(receivedObj)

        optionHandler = MenuOptionHandler(
            loadedData, clientSocket, address)
        optionHandler.manageOption()

    print(f"Closed Connection to {address}")
