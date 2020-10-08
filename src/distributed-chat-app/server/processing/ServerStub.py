import json
import time


class ServerStub:
    server_socket = None

    def __init__(self, server_socket):
        self.startTime = time.time()
        ServerStub.server_socket = server_socket

    def sendMessage(self, msg: str) -> bool:
        try:
            self.server_socket.sendall(msg.encode('utf-8'))
        except Exception as e:
            print(f"(ERROR) could not send message\n{e}")
            return False
        return True

    @staticmethod
    def receiveMessage(max_size: int, client_socket) -> bytes:
        while True:
            try:
                return client_socket.recv(max_size)
            except BlockingIOError:
                pass

    @staticmethod
    def encode(obj):
        """Encode object to be sent to client"""
        return str.encode(json.dumps(obj))

    @staticmethod
    def decode(obj):
        """Decode object received from server"""
        return json.loads(obj)
