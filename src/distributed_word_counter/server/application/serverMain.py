import logging
import sys
from connection.ServerConnector import ServerConnector


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    HOST = ""
    PORT = int(sys.argv[1])
    CON_TIMEOUT = 15
    LISTEN_BACKLOG = 5
    connector = ServerConnector(HOST, PORT, LISTEN_BACKLOG, CON_TIMEOUT)
    connector.acceptConnections()
    logging.info(f"Closed Connection to {connector.address}")
