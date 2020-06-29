import logging
from ClientConnector import ClientConnector


if __name__ == "__main__":
    ClientConnector.tryConnection()

    logging.info("Client is closing connection")
