import re
from .formula import Formula
from .truth_assignment import TruthAssignment
from .propositional_variable import PropositionalVariable

class Literal(Formula):
    def __init__(self, prop_var:PropositionalVariable, is_negated:bool=False):
        self.prop_var = prop_var
        self.is_negated = is_negated

    def __eq__(self, obj: object, /) -> bool:
        if not isinstance(obj, Literal):
            return NotImplemented
        return self.prop_var == obj.prop_var and self.is_negated == obj.is_negated

    def __hash__(self) -> int:
        return hash(self.prop_var)

    def __invert__(self):
        return Literal(self.prop_var, not self.is_negated)

    def to_latex(self)->str:
        match = re.fullmatch(r'([A-Za-z]+)(\d+)', self.prop_var.name)
        if match is None:
            return f'{self.prop_var.name}'
        string, number = match.groups()
        if self.is_negated:
            return rf'\lnot \ {string}_{{{number}}}'
        return rf'{string}_{{{number}}}'

    def __str__(self) -> str:
        return self.to_latex()

    def __repr__(self)->str:
        match = re.fullmatch(r'([A-Za-z]+)(\d+)', self.prop_var.name)
        if match is None:
            return f'${self.prop_var.name}$'
        string, number = match.groups()
        if self.is_negated:
            return f'not {string}_{number}'
        return f'{string}_{number}'

    def _repr_latex_(self)->str:
        return f'${self.to_latex()}$'

    def get_prop_vars(self) ->list[PropositionalVariable]:
        return [self.prop_var]

    def evaluate(self, truth_assignment:TruthAssignment) -> bool:
        truth_value = truth_assignment.get_truth_values([self.prop_var])
        if self.is_negated:
            return not truth_value[self.prop_var]
        return truth_value[self.prop_var]

    def satisfy(self)->TruthAssignment:
        return TruthAssignment({self.prop_var: not self.is_negated})