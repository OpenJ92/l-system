from typing import Protocol, runtime_checkable
from lsystems.protocols.sentence import Sentence

@runtime_checkable
class Production(Protocol):
    def __call__(self, symbol: Hashable, scope: ScopeBundle) -> Sentence: ...
