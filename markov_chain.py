import re
import random


class MarkovChain:
    def __init__(self):
        self.words = {}
        self.starts = {}

    def _update_starts(self, word: str):
        if word not in self.starts:
            self.starts[word] = 1
        else:
            self.starts[word] += 1

    def _update_words(self, word: str, next_w: str | None):
        if word not in self.words:
            self.words[word] = {}
        if next_w not in self.words[word]:
            self.words[word][next_w] = 1
        else:
            self.words[word][next_w] += 1

    def space_ponctuation(self, text: str):
        for k in ".,!?":
            text = text.replace(f" {k}", f"{k}")
        for k in "'":
            text = text.replace(f" {k} ", f"{k}")
        return text

    def generator_clean_text(self, text: str):
        for line in text.splitlines():
            yield list(filter(lambda w: w and w.strip(), re.split("(\W)", line)))

    def add_text(self, text: str):
        for line in self.generator_clean_text(text):
            if not line:
                continue
            self._update_starts(line[0])
            prev_w = None
            for i in range(len(line) - 1):
                self._update_words(line[i], line[i + 1])
                if prev_w:
                    self._update_words("+".join([prev_w, line[i]]), line[i + 1])
                prev_w = line[i]
            self._update_words(line[-1], None)
            if len(line) > 1:
                self._update_words("+".join([line[-2], line[-1]]), None)

    def generate_text(self, seed: int = None, max_len: int = 100):
        text = []
        if seed:
            random.seed(seed)
        curr = random.choices(
            population=list(self.starts.keys()),
            weights=[float(self.starts[k] / len(self.starts)) for k in self.starts],
        )[0]
        text.append(curr)
        prev_w = None
        for _ in range(max_len):
            tmp = curr
            curr_w = "+".join(filter(None, [prev_w, curr]))
            if curr_w not in self.words:
                break
            sum_weights = 0
            for k in self.words[curr_w]:
                sum_weights += self.words[curr_w][k]
            curr = random.choices(
                population=list(self.words[curr_w].keys()),
                weights=[float(self.words[curr_w][k] / sum_weights) for k in self.words[curr_w]],
            )[0]
            if not curr:
                break
            text.append(curr)
            prev_w = tmp
        generated_text = " ".join(text)
        return self.space_ponctuation(generated_text)


mc = MarkovChain()
with open("tweets.txt", "r") as f:
    mc.add_text(f.read())
print(mc.generate_text())
