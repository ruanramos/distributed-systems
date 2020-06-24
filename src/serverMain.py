import sys
from distributed_word_counter.server.counterServerConnection import Connector
from distributed_word_counter.server.counterServerLogic import OptionHandler

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
        receivedOption = int(str(clientSocket.recv(1024), 'utf8'))
        print(f"You chose option {receivedOption}")

        optionHandler = OptionHandler(receivedOption, clientSocket)
        optionHandler.manageOption()

    print(f"Closed Connection to {address}")
