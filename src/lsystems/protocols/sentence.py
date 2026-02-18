from __future__ import annotations
from typing import Protocol, runtime_checkable, Self
from collections.abc import Sequence, Hashable

class Sentence(Protocol, Sequence[Hashable]):
    @classmethod
    def empty(self): ...
    
    def combine(self, other: Self) -> Self: ...
    def clone(self) -> Self: ...
