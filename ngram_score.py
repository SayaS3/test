
import math

class NgramScore(object):
    def __init__(self, ngramfile, sep=' '):
        self.ngrams = {}
        for line in open(ngramfile):
            key, count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        for key in self.ngrams.keys():
            self.ngrams[key] = math.log10(float(self.ngrams[key]) / self.N)
        self.floor = math.log10(0.01 / self.N)

    def score(self, text):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score
