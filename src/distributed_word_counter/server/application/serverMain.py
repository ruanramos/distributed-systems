import sys
from connection.ServerConnector import ServerConnector


if __name__ == "__main__":
    HOST = ""
    PORT = int(sys.argv[1])
    CON_TIMEOUT = 15
    LISTEN_BACKLOG = 5
    connector = ServerConnector(HOST, PORT, LISTEN_BACKLOG, CON_TIMEOUT)
    connector.acceptConnections()
    print(f"Closed Connection to {connector.address}")
