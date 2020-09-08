import logging
from ClientConnector import ClientConnector

if __name__ == "__main__":
    # Client program entry point.
    ClientConnector.tryConnection()

    logging.info("Client is closing connection")
