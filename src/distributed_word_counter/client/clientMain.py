import logging
from ClientConnector import ClientConnector
from ClientScreenPrinter import ClientScreenPrinter

if __name__ == "__main__":
    # Client program entry point.
    ClientConnector.tryConnection()
    ClientScreenPrinter.confirmConnected()
