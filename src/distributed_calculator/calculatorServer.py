import socket
import time

# For Server socket, always use this order
# socket()
# bind()
# listen()
# accept() -> can loop

HOST = ""
PORT = 50002
CON_TIMEOUT = 15
validOperators = ['-', '+', '*', '/']

def oldCode():
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    #oldCode()
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST, socket.gethostname(), socket.gethostbyname(socket.gethostname()))
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)

    while True:
        # waits for first connection can be blocking
        print(f"Server is waiting for client connection. Timeout in {CON_TIMEOUT} seconds")
        serverSocket.settimeout(CON_TIMEOUT)
        clientSocket, address = serverSocket.accept()
        
        with clientSocket:
            print('Connected by', address)
            
            while True:
                dataReceived = clientSocket.recv(1024)  # waits for data, can be blocking
                if not dataReceived:
                    break
                receivedExpression = str(dataReceived, 'utf8')                
                try:
                    result = str(eval(receivedExpression))
                    print("Server sent the answer: " + result)
                    clientSocket.send(bytes(result, 'utf8'))
                except:
                    if receivedExpression == 'q':
                        print("Connection closed")
                        clientSocket.send(b"c")
                        break
                    print("error on eval")
                    clientSocket.send(b"error")