import time
from utils.constants import MESSAGE_TYPES


class Message:
    """
    Message exchange will be as follows:
    message = {
        TYPE,      --> '1'             = 50 bytes
        TIMESTAMP, --> time.asctime()  = 73 bytes
        FROM,      --> (address, port) = 64 bytes
        TO,        --> (address, port) = 64 bytes
        VALUE      --> variable string
    } using sys.getSizeof()
    """

    def __init__(self, msg_type: str, value: str, sender: tuple, receiver: tuple):
        self.type = msg_type
        self.sender = sender
        self.receiver = receiver
        self.time = time.asctime()
        self.value = value
