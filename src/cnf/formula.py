from __future__ import annotations
from abc import ABC, abstractmethod
from .propositional_variable import PropositionalVariable


class Formula(ABC):
    @abstractmethod
    def __eq__(self, obj:object, /)->bool:
        ...

    @abstractmethod
    def __hash__(self)->int:
        ...

    @abstractmethod
    def to_latex(self):
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self)->str:
        ...

    @abstractmethod
    def get_prop_vars(self)->list[PropositionalVariable]:
        ...

    @abstractmethod
    def _repr_latex_(self):
        ...

    @abstractmethod
    def evaluate(self, truth_assignment:TruthAssignment)->bool:
        ...

    @abstractmethod
    def satisfy(self)->TruthAssignment:
        ...
