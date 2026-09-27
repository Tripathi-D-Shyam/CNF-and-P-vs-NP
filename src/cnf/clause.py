from .literal import Literal
import typing


class Clause:
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


    def to_latex(self):
        seperator = r' \lor ' if self.clause_type == 'Disjunctive' else r' \land '
        return seperator.join(f'{str(literal)}' for literal in self.literals)

    def __str__(self) -> str:
        return self.to_latex()

    def __repr__(self) -> str:
        seperator = ' or ' if self.clause_type == 'Disjunctive' else ' and '
        return seperator.join(f'{str(literal)}' for literal in self.literals)

    def _repr_latex_(self):
        return f'${self.to_latex()}$'