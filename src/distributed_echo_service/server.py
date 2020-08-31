import socket

if __name__ == "__main__":
    HOST = "" # default communication interface
    PORT = 5001
    CON_TIMEOUT = 15
    NUM_CLIENTS = 5

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        HOST = socket.gethostbyname(socket.gethostname())
        print(HOST, socket.gethostname())
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(NUM_CLIENTS)

        while True:
            # waits for first connection can be blocking
            print(f"Server is waiting for client connection. Timeout in {CON_TIMEOUT} seconds")
            serverSocket.settimeout(CON_TIMEOUT)
            clientSocket, address = serverSocket.accept()

            with clientSocket:
                print("Connected by", address)
                while True:
                    messageReceived = clientSocket.recv(1024)  # waits for data, can be blocking
                    if not messageReceived:
                        break
                    print(f"Message received from client")
                    clientSocket.send(messageReceived)
                    print("Message sent back to client")
                
                print("Client closed connection")