import socket


HOST = socket.gethostname()
PORT = 5001


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, PORT))
        print(f"Client connected to server at port {PORT} and host {HOST}")

        while True:
            msg = input("Send a message: ")
            clientSocket.send(bytes(msg, 'utf8'))
            print("Message delivered to server, waiting for response .....")
            receivedMessage = clientSocket.recv(1024)
            print(f"Message received back from server: {str(receivedMessage, 'utf8')}")

        print("Client is closing connection")