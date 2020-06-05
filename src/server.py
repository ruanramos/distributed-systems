import socket
import time

# For Server socket, always use this order
# socket()
# bind()
# listen()
# accept() -> can loop

HOST = ""
PORT = 50017

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    # waits for first connection can be blocking
    conn, address = serverSocket.accept()
    with conn:
        print('Connected by', address)
        while True:
            data = conn.recv(1024)  # waits for message, can be blocking
            if not data:
                break
            print("Yes, I'm the server. I'm waiting for "
                  + str(data)
                  + " seconds")
            time.sleep(int(data))
            conn.send(b"2")
