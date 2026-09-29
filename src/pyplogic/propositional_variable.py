import re
from typing import Self


class PropositionalVariable:
    __instances = {}
    def __new__(cls, name) -> Self:
        if name not in cls.__instances:
            obj = super().__new__(cls)
            cls.__instances[name] = obj
        return cls.__instances[name]

    @classmethod
    def get_instances(cls)->list[Self]:
        return list(cls.__instances.values())

    def __init__(self, name:str) -> None:
        if hasattr(self, '_initialized'):
            return
        self.name = name
        self._initialized = True

    def __eq__(self, obj:object, /)->bool:
        if not isinstance(obj, PropositionalVariable):
            return NotImplemented
        return self.name == obj.name

    def __hash__(self)->int:
        return hash(self.name)

    def __repr__(self)->str:
        match = re.fullmatch(r'([A-Za-z]+)(\d+)', self.name)
        if match is None:
            return f'${self.name}$'
        string, number = match.groups()
        return f'{string}_{number}'
