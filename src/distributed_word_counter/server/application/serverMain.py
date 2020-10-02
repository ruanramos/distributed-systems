import logging
import sys
from connection.ServerConnector import ServerConnector

if __name__ == "__main__":
    """Server entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    HOST = ""
    PORT = int(sys.argv[1])
    CON_TIMEOUT = 15
    LISTEN_BACKLOG = 5
    serverConnector = ServerConnector(HOST, PORT, LISTEN_BACKLOG, CON_TIMEOUT)
    serverConnector.accept_connections()
    logging.info(f"Closed Connection to {serverConnector.address}")
