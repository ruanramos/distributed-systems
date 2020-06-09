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
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST, socket.gethostname(), socket.gethostbyname(socket.gethostname()))
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    # waits for first connection can be blocking
    serverSocket.settimeout(5)
    conn, address = serverSocket.accept()
    with conn:
        receivedNumbers = []
        print('Connected by', address)
        for i in range(3):
            conn.settimeout(5)
            data = conn.recv(1024)  # waits for message, can be blocking
            if not data:
    	        break
            receivedNumbers.append(int(str(data, 'utf8')))
                
        print("Server will now send the numbers received multiplied by 4")
        ans = ""
        for i in receivedNumbers:
            ans += str(i * 4)  + " "
        conn.send(bytes(ans, 'utf8'))

