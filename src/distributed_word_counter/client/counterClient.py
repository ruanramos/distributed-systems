import socket

if __name__ == "__main__":
    hostname = socket.gethostname()
    HOST = hostname
    PORT = 50002

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, PORT))
        print("Client connected to server!")
        while True:
            clientSocket.send(bytes(getExpression(), 'utf8'))
            result = clientSocket.recv(1024)
            result = str(result, 'utf8')
            if result == "c":
                break
            print("Result: " + result)
        print("Client is closing connection")