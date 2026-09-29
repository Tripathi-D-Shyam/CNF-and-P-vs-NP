from typing import Self

from .formula import Formula
from .propositional_variable import PropositionalVariable
class TruthAssignment:
    all_prop_vars: list[PropositionalVariable] = PropositionalVariable.get_instances()

    def __init__(self, truth_values:dict[PropositionalVariable, bool]|None=None) -> None:
        self.truth_values = {prop: True for prop in self.all_prop_vars}
        if truth_values is None:
            return
        for prop in truth_values.keys():
            self.truth_values[prop] = truth_values[prop]

    def set_truth_assignment(self, truth_assignment:Self)->None:
        for prop in truth_assignment.truth_values.keys():
            self.truth_values[prop] = truth_assignment.truth_values[prop]

    def get_localized_dict(self, formula:Formula)->dict[PropositionalVariable, bool]:
        return {prop: self.truth_values[prop] for prop in formula.get_prop_vars()}

    def __eq__(self, obj:object)->bool:
        if not isinstance(obj, TruthAssignment):
            return NotImplemented
        return self.truth_values == obj.truth_values

    def get_truth_values(self, props:list[PropositionalVariable])->dict[PropositionalVariable, bool]:
        return {prop: self.truth_values[prop] for prop in props}

    def set_truth_values(self, assigned_truth:dict[PropositionalVariable, bool])->None:
        for prop in assigned_truth:
            self.truth_values[prop] = assigned_truth[prop]