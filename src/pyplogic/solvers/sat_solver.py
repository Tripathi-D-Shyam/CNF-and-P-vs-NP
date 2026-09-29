from abc import ABC, abstractmethod
from cnf.formula import Formula

class SATSolver(ABC):
    @abstractmethod
    def __init__(self, formula:Formula):
        self.formula = formula

    @abstractmethod
    def satisfiable(self)->bool:
        ...

    #@abstractmethod
    # I plan to implement one