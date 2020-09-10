import re


class TextAnalizer():
    """Handles analysis logic"""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def getWordsCount(self):
        """Splits and counts words in the text"""
        count = {}
        for word in re.split('[ ,.!?"\n-]+', self.text):
            if word.upper() in count:
                count[word.upper()] += 1
            else:
                count[word.upper()] = 1
        return count

    def analize(self, numberOfWords):
        """Processing of the counting. Sort and then Get top ones"""
        obj = {}
        sortedCount = {k: v for k, v in sorted(
            self.getWordsCount().items(),
            key=lambda item: item[1],
            reverse=True
        )}
        for i, j in enumerate(sortedCount.items()):
            if i >= numberOfWords:
                break
            obj[i] = j
        return obj
