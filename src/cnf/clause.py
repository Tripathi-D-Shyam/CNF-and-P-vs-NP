from .literal import Literal
import typing
from .formula import Formula
from .propositional_variable import PropositionalVariable
from .truth_assignment import TruthAssignment

class Clause(Formula):
    def __init__(
            self,
            literals:list[Literal]|None=None,
            clause_type:typing.Literal['Conjunctive', 'Disjunctive']='Disjunctive',
    ):
        if clause_type not in ['Conjunctive', 'Disjunctive']:
            raise ValueError('clause_type must be "Conjunctive" or "Disjunctive"')
        self.literals:list[Literal] = [] if literals is None else literals
        self.clause_type = clause_type

    def __hash__(self) -> int:
        return hash(*self.literals)

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, Clause):
            return NotImplemented
        return set(self.literals) == set(other.literals)


    def to_latex(self)->str:
        seperator = r' \lor ' if self.clause_type == 'Disjunctive' else r' \land '
        return seperator.join(f'{str(literal)}' for literal in self.literals)

    def __str__(self) -> str:
        return self.to_latex()

    def __repr__(self) -> str:
        seperator = ' or ' if self.clause_type == 'Disjunctive' else ' and '
        return seperator.join(f'{str(literal)}' for literal in self.literals)

    def _repr_latex_(self):
        return f'${self.to_latex()}$'

    def evaluate(self, truth_assignment:TruthAssignment)->bool:
        assigned_truth = truth_assignment.get_truth_values([literal.prop_var for literal in self.literals])
        if self.clause_type == 'Disjunctive':
            return all(assigned_truth)
        else:
            return any(assigned_truth)

    def get_prop_vars(self) ->list[PropositionalVariable]:
        prop_vars = []
        for literal in self.literals:
            prop_vars.extend(literal.get_prop_vars())
        return prop_vars

    def satisfy(self)->TruthAssignment:
        ta = TruthAssignment()
        for literal in self.literals:
            ta.set_truth_assignment(literal.satisfy())
        return ta