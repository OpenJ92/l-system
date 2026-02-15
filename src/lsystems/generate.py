class Generate():
    def __init__(self, lsystem: LSystem, depth: int, context: Context):
        self.lsystem = lsystem
        self.depth = depth
        self.context = context

    def run_generation(self, generation: int):
        alphabet = self.lsystem.alphabet
        productions = self.lsystem.productions
        sentence = self.lsystem.sentence

        rewrites = []
        for index, symbol in enumerate(sentence):
            production = productions.get(symbol)
            context = self.context.evolve(sentence, index, generation)
            rewrites.append(production(symbol, context))

        sentence = sentence.empty()
        for rewrite in rewrites:
            sentence = sentence.combine(rewrite)

        return sentence

    def run(self):
        sentence = self.lsystem.sentence
        for generation in range(self.depth):
            sentence = self.run_generation(generation)
        return sentence
            

def Run(generate: Generate):
    return generate.run()
