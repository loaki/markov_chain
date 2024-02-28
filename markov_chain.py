import re
import random

class MarkovChain:
    def __init__(self):
        self.words = {}
        self.starts = {}
        self.ponctuation = "!#$%&()*+,./:;<=>?@[']^_{|}~\\','"

    def generator_clean_text(self, text: str):
        for line in text.splitlines():
            yield list(filter(lambda w: w and w.strip(), re.split("(\W)", line)))

    def add_text(self, text: str):
        for line in self.generator_clean_text(text):
            if not line:
                continue
            if line[0] not in self.starts:
                self.starts[line[0]] = 1
            else:
                self.starts[line[0]] += 1
            for i in range(len(line) - 1):
                if line[i] not in self.words:
                    self.words[line[i]] = {}
                if line[i + 1] not in self.words[line[i]]:
                    self.words[line[i]][line[i + 1]] = 1
                else:
                    self.words[line[i]][line[i + 1]] += 1
            if line[-1] not in self.words:
                self.words[line[-1]] = {}
                self.words[line[-1]][None] = 1
            else:
                self.words[line[-1]][None] += 1

    def generate_text(self, seed: int = None, max_len: int = 10):
        text = []
        if seed:
            random.seed(seed)
        curr = random.choices(population=list(self.starts.keys()), weights=[float(self.starts[k] / len(self.starts)) for k in list(self.starts.keys())])[0]
        text.append(curr)
        for _ in range(max_len):
            if curr not in list(self.words.keys()):
                break
            sum_weights = 0
            for k in self.words[curr].keys():
                sum_weights += self.words[curr][k]
            curr = random.choices(population=list(self.words[curr].keys()), weights=[float(self.words[curr][k] / sum_weights) for k in list(self.words[curr].keys())])[0]
            if not curr:
                break
            text.append(curr)
        return " ".join(text)


mc = MarkovChain()
with open("data.txt", "r") as f:
    mc.add_text(f.read())
print(mc.generate_text())

