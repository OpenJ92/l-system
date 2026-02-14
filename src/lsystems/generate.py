class Generate():
    def __init__(self, lsystem: LSystem, depth: int, context: Context):
        self.lsystem = lsystem
        self.depth = depth
        self.context = context

    def run_generation(self):
        alphabet = self.lsystem.alphabet
        productions = self.lsystem.productions
        sentence = self.lsystem.sentence

        rewrites = []
        for letter in sentence:
            production = productions.get(letter)
            rewrite = production(letter, context)
            rewrites.append(rewrite)

        sentence = alphabet.empty()
        for rewrite in rewrites:
            sentence = alphabet.combine(sentence, rewrite)

        return sentence

    def run(self):
        sentence = self.lsystem.sentence
        for _ in range(self.depth):
            sentence = self.run_generation()
            

def Run(generate: Generate):
    return generate.run()
