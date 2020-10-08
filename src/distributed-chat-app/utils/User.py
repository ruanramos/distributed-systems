class User:

    idCounter = 0

    def __init__(self, username):
        self.username = username
        self.id = User.idCounter + 1
        User.idCounter += 1
