import json
import time
from application.UserInteraction import UserInteraction
from utils.Message import Message


class ClientStub:

    def __init__(self, socket):
        self.sock = socket

    def sendMessage(self, msg: bytes) -> bool:
        try:
            self.sock.sendall(msg)
        except Exception as e:
            UserInteraction.handleError(error=e)
            return False
        return True

    def receiveMessage(self, max_size: int) -> bytes:
        return self.sock.recv(max_size)

    @staticmethod
    def encode(obj):
        """Encode object to be sent to client"""
        return str.encode(json.dumps(obj))

    @staticmethod
    def decode(obj):
        """Decode object received from server"""
        return json.loads(obj)

    def subscription(self, status: str):
        """ 1 to subscribe, 0 to unsubscribe """
        message = Message('1', status, self.sock.getsockname(), self.sock.getpeername())
        self.sendMessage(self.encode(message.__dict__))

    @staticmethod
    def wait():
        while True:
            time.sleep(2)
            print("waiting....")