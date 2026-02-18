class LSystem():
    def __init__(self, alphabet: set[Hashable], productions: Productions, sentence: Sentence):
        self.alphabet = alphabet
        self.productions = productions
        self.sentence = sentence
