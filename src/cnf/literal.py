import re

class Literal:
    def __init__(self, literal_id:str, is_negated:bool=False):
        self.literal_id = literal_id
        self.is_negated = is_negated

    def __eq__(self, obj: object, /) -> bool:
        if not isinstance(obj, Literal):
            return NotImplemented
        return self.literal_id == obj.literal_id and self.is_negated == obj.is_negated

    def __hash__(self) -> int:
        return hash(self.literal_id)

    def __invert__(self):
        return Literal(self.literal_id, not self.is_negated)

    def to_latex(self)->str:
        string, number = re.fullmatch(r'([A-Za-z]+)(\d+)', self.literal_id).groups()
        if self.is_negated:
            return rf'\lnot \ {string}_{{{number}}}'
        return rf'{string}_{{{number}}}'

    def __str__(self) -> str:
        return self.to_latex()

    def __repr__(self):
        string, number = re.fullmatch(r'([A-Za-z]+)(\d+)', self.literal_id).groups()
        if self.is_negated:
            return f'not {string}_{number}'
        return f'{string}_{number}'

    def _repr_latex_(self):
        return f'${self.to_latex()}$'