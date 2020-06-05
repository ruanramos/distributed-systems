import socket

# For Client socket, always use this order:
# socket()
# connect()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

HOST = 'localhost'
PORT = 50017

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((HOST, PORT))
    print('Hello, are you the server? I am ' + HOST)
    print("Can you wait for some seconds?")
    clientSocket.send(b"5")
    data = clientSocket.recv(1024)
    print("Ok, I got your number. It was ", int(data))
