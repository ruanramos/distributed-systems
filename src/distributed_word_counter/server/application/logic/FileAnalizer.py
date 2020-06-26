class TextAnalizer():

    def __init__(self, text):
        super().__init__()
        self.text = text

    def getWordsCount(self):
        count = {}
        for word in self.text.split():
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
        return count

    def analize(self, numberOfWords):
        # Analize logic here
        obj = {}
        sortedCount = {k: v for k, v in sorted(
            self.getWordsCount().items(), key=lambda item: item[1], reverse=True)}
        for i, j in enumerate(sortedCount.items()):
            if i >= numberOfWords:
                break
            obj[i] = j
        return obj
