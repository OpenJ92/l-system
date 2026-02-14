class LSystem():
    def __init__(self, alphabet: Alphabet, productions: Productions, sentence: Sentence):
        self.alphabet = alphabet
        self.productions = productions
        self.sentence = sentence
