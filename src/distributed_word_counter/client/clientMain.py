import socket
import sys


def showMenu():
    print("""
            1- See saved files
            2- Choose a file to analize
            3- Create a new file
            4- Quit
            """)


def validOption(option):
    return int(option) in range(1, 5)


def getOption():
    option = input()
    while not validOption(option):
        print("Invalid option. Please choose a valid option")
        showMenu()
        option = input()
    return option


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = int(sys.argv[1])
        clientSocket.connect((HOST, PORT))
        print("Client connected to server!")

        # while True:
        showMenu()
        option = getOption()
        clientSocket.send(bytes(option, 'utf8'))

        answer = clientSocket.recv(1024)
        receivedData = str(answer, 'utf8').split("\n")
        if receivedData[0] == "close":
            print("Quiting program!")
            exit(0)
        elif receivedData[0] == "list":
            print("--------- These are the saved files --------\n\n")
            print(str(answer, 'utf8'))
            print("\n\n--------------------------------------------\n\n")
        elif receivedData[0] == "analize":
            # Show analizes info here
            pass

    print("Client is closing connection")
