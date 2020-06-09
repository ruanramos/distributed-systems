import socket

# For Client socket, always use this order:
# socket()
# connect()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

HOST = hostname
PORT = 50017

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.settimeout(5)
    clientSocket.connect((HOST, PORT))
    print("Client connected to server!")
    for i in range(3):
        clientSocket.settimeout(5)
        clientSocket.send(bytes(input("Enter a number"), 'utf8'))

    clientSocket.settimeout(5)
    data = clientSocket.recv(1024)
    print("Client received answer: " + str(data, 'utf8'))
