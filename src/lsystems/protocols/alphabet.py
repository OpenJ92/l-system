from typing import Protocol
from collections.abc import Set, Hashable

class Alphabet(Protocol, Set[Hashable]):
    def boundary(self) -> Hashable: ...
