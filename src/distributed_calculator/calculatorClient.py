import socket

# For Client socket, always use this order:
# socket()
# connect()

def getNumbers():
    numbers = []
    # kinda hardcoded for only 2 numbers and 1 operation
    for _ in range(2):
        n = input("Give a number: ")
        while not n.isnumeric:
            n = input("Give a valid number: ")
        numbers.append(n)
    return numbers

def getOperator():
    operator = input("Send an operator: ")
    while operator not in validOperators:
        operator = input("Send one of the four valid operators (+, -, /, *): ")
    return operator

def constructMessage(it):
    message = ""
    for i in it:
        message += i + " "
    return message

if __name__ == "__main__":
    hostname = socket.gethostname()
    validOperators = ['-', '+', '*', '/']

    HOST = hostname
    PORT = 50017

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, PORT))
        print("Client connected to server!")
        while True:
            clientSocket.send(bytes(constructMessage(getNumbers()), 'utf8'))
            operator = getOperator()
            clientSocket.send(bytes(operator, 'utf8'))
            result = clientSocket.recv(1024)
            print("Result: " + str(result, 'utf8'))