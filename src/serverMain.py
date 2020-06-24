import sys
from distributed_word_counter.server.counterServerConnection import Connector

if __name__ == "__main__":
    HOST = ""
    PORT = int(sys.argv[1])
    CON_TIMEOUT = 15
    LISTEN_BACKLOG = 5
    connector = Connector(HOST, PORT, LISTEN_BACKLOG, CON_TIMEOUT)
    connector.acceptConnections()
    print(f"Closed Connection to {connector.address}")
