from typing import Protocol

class Sentence(Protocol):
    def combine(self, other):
        raise NotImplementedError

    def mempty(self):
        raise NotImplementedError
