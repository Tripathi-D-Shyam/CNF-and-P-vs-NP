import typing
from .literal import Literal
from .clause import Clause
from .formula import Formula
from .propositional_variable import PropositionalVariable
from .truth_assignment import TruthAssignment

class NormalForm(Formula):
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

    def parse_str(self, string:str)->None:

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
                #It might happen that a normal form not supported
                #by this parse method happens to be input
                #this will cause incorrect parsing that too silently,
                #I plan to implement error in such a scenario to be thrown.
                literal_id, *literal_negator = literal_cleaned.split(' ')[::-1]
                prop_var = PropositionalVariable(literal_id)
                literal_obj = Literal(prop_var, bool(literal_negator))
                clause_obj.literals.append(literal_obj)
            self.clauses.append(clause_obj)

    def to_latex(self)->str:
        if self.normal_form_type == 'Conjunctive':
            seperator = r' \land '
        else:
            seperator = r' \lor '
        return seperator.join(f'({str(clause)})' for clause in self.clauses)

    def __eq__(self, obj:object)->bool:
        if not isinstance(obj,NormalForm):
            return NotImplemented
        return set(self.clauses) == set(self.clauses) and self.normal_form_type == obj.normal_form_type

    def __hash__(self) ->int:
        return hash(*self.clauses, self.normal_form_type)

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

    def get_prop_vars(self) ->list[PropositionalVariable]:
        prop_vars = []
        for clause in self.clauses:
            prop_vars.extend(clause.get_prop_vars())
        return prop_vars


    def evaluate(self, truth_assignment:TruthAssignment)->bool:
        if self.normal_form_type == 'Conjunctive':
            return all([clause.evaluate(truth_assignment) for clause in self.clauses])
        else:
            return any([clause.evaluate(truth_assignment) for clause in self.clauses])

    def satisfy(self)->TruthAssignment:
        ta = TruthAssignment()
        for clause in self.clauses:
            ta.set_truth_assignment(clause.satisfy())
        return ta