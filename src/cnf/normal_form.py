import typing
from .literal import Literal
from .clause import Clause

class NormalForm:
    def __init__(
            self,
            clauses:list[Clause]|None=None,
            normal_form_type:typing.Literal['Conjunctive', 'Disjunctive']='Conjunctive',
            and_str:str='and',
            or_str:str='or',
            not_str:str='not',
            left_punc:str='(',
            right_punc:str=')'
    ):
        if normal_form_type not in ['Conjunctive', 'Disjunctive']:
            raise ValueError('normal_form_type must be either Conjunctive or Disjunctive')
        self.clauses:list[Clause] = [] if clauses is None else clauses
        self.normal_form_type = normal_form_type
        self.and_str = and_str
        self.or_str = or_str
        self.not_str = not_str
        self.left_punc = left_punc
        self.right_punc = right_punc

    def parse_str(self, string:str):

        if self.normal_form_type == 'Conjunctive':
            primary_sep = self.and_str
            secondary_sep = self.or_str
        else:
            primary_sep = self.or_str
            secondary_sep = self.not_str

        for clause in string.strip().split(primary_sep):
            clause_cleaned = (clause
                              .strip()
                              .strip(self.left_punc)
                              .strip(self.right_punc)
                              )
            clause_obj = Clause()

            for literal in clause_cleaned.strip().split(secondary_sep):
                literal_cleaned = literal.strip()
                literal_id, *literal_negator = literal_cleaned.split(' ')[::-1]
                literal_obj = Literal(literal_id, bool(literal_negator))
                if literal_obj not in self.clauses:
                    clause_obj.literals.append(literal_obj)


                # I plan to implement custom error
                # NotValidForm to raise in a situation
                # such as this

            if clause_obj not in self.clauses:
                self.clauses.append(clause_obj)

    def to_latex(self)->str:
        if self.normal_form_type == 'Conjunctive':
            seperator = r' \land '
        else:
            seperator = r' \lor '
        return seperator.join(f'({str(clause)})' for clause in self.clauses)

    def __str__(self) -> str:
        return self.to_latex()

    def __repr__(self)->str:
        if self.normal_form_type == 'Conjunctive':
            seperator = ' and '
        else:
            seperator = ' or '
        return seperator.join(f'({str(clause)})' for clause in self.clauses)

    def _repr_latex_(self):
        return f'${self.to_latex()}$'