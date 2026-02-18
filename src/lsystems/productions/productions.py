from lsystems.productions.static import Static

class Productions():
    def __init__(self, sentence_type):
        self.productions = {}
        self.lift = sentence_type.lift

    def add(self, symbol, production):
        self.productions[symbol] = production

    def get(self, symbol):
        return self.productions.get(symbol, Static(self.lift(symbol)))
