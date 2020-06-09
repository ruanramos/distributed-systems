import socket

# For Client socket, always use this order:
# socket()
# connect()

hostname = socket.gethostname()
validOperators = ['-', '+', '*', '/']

HOST = hostname
PORT = 50017

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((HOST, PORT))
    print("Client connected to server!")
    while True:    
        numbers = []
        # kinda hardcoded for only 2 numbers and 1 operation
        for i in range(2):
            n = input("Give a number: ")
            while not n.isnumeric:
                n = input("Give a valid number: ")
            numbers.append(n)
        numbersMessage = ""
        for number in numbers:
            numbersMessage += number + " "
        clientSocket.send(bytes(numbersMessage, 'utf8'))

        operator = input("Send an operator: ")
        while operator not in validOperators:
            operator = input("Send one of the four valid operators (+, -, /, *): ")
        clientSocket.send(bytes(operator, 'utf8'))

        result = clientSocket.recv(1024)
        print("Result: " + str(result, 'utf8'))
