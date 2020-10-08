DEFAULT_SERVER_PORT = 9001
DEFAULT_HOST = ''  # Empty string indicates the server can receive requests from any network interface
NUMBER_OF_CLIENTS = 20
MENU_OPTIONS = {'1': 'Enter chat', '2': 'Quit'}
MENU_TEXT = "Welcome to the chat app. Choose an option below:"


""" 
Message exchange will be as follows:
message = {
    TYPE,      --> '1'             = 50 bytes
    TIMESTAMP, --> time.asctime()  = 73 bytes
    FROM,      --> (address, port) = 64 bytes 
    TO,        --> (address, port) = 64 bytes
    VALUE      --> variable string
} using sys.getSizeof()

Types have predefined message sizes in bytes. Example:
message = {224, 1} --> represents a subscribe 
message = {224, 0} --> represents an unsubscribe 
"""
MESSAGE_TYPES = {'SUBSCRIPTION': '1', 'CHAT_MESSAGE': '2'}

ON = '1'
OFF = '0'
