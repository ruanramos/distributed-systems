import json


def composeMessage(*pairs):
    message = {}
    for pair in pairs:
        message[pair[0]] = pair[1]
    return str.encode(json.dumps(message))


def addToMessage(previousMessage, *pairs):
    for pair in pairs:
        previousMessage[pair[0]] = pair[1]
    return str.encode(json.dumps(previousMessage))


if __name__ == "__main__":
    print(composeMessage(("filename", "bla.txt"), ("answer", "close")))
    print(addToMessage({"Car": "celta"},
                       ("filename", "bla.txt"), ("answer", "close")))
