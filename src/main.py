from distributed_word_counter.server.counterServerConnection import Connector

HOST = ""
PORT = 50011
CON_TIMEOUT = 15


if __name__ == "__main__":
    connector = Connector(HOST, PORT, CON_TIMEOUT)
    clientSocket, address = connector.listenToClients()

    with clientSocket:
        print('Connected by', address)
        # waits for menu option
        receivedOption = int(str(clientSocket.recv(1024), 'utf8'))
        print(f"You chose option {receivedOption}")

        #optionHandler = OptionHandler(receivedOption)

        if receivedOption == 4:
            clientSocket.send(bytes("close", 'utf8'))

    print(f"Closed Connection to {address}")
