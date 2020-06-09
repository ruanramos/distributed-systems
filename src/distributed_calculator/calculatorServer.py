import socket
import time

# For Server socket, always use this order
# socket()
# bind()
# listen()
# accept() -> can loop

HOST = ""
PORT = 50017
validOperators = ['-', '+', '*', '/']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST, socket.gethostname(), socket.gethostbyname(socket.gethostname()))
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    
    while True:
        # waits for first connection can be blocking
        clientSocket, address = serverSocket.accept()
        
        with clientSocket:
            print('Connected by', address)
            
            while True:
                receivedNumbers = []
                dataReceived = clientSocket.recv(1024)  # waits for data, can be blocking
                if not dataReceived:
                    break
                receivedNumbers = str(dataReceived, 'utf8').split()
                print(receivedNumbers)
                print('Received Numbers ' + receivedNumbers[0] + " and " + receivedNumbers[1])
                
                operatorReceived = clientSocket.recv(1024) # waits for operation
                if not operatorReceived:
                    break
                operatorReceived = str(operatorReceived, 'utf8')
                print('Received operator ' + operatorReceived)
                
                result = str(eval(receivedNumbers[0] + operatorReceived + receivedNumbers[1]))
                        
                print("Server sent the answer: " + result)
                clientSocket.send(bytes(result, 'utf8'))
    print("Connection to " + address + " closed")