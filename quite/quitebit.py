from __future__ import annotations
import random

NoneType = type(None)


class QuiteBit(object):
    def __init__(self, chance: int = 0.5,
                 superposition: bool = True, value: NoneType | int = None):
        self.chance = chance
        self.superposition = superposition
        self._value = value

    def meter(self):
        self.superposition = False
        self.value = 1 if random.random() <= self.chance else 0

        return self.value

    def double(self):
        qbit, wbit = None, None
        if self.superposition:
            chance = self.chance

            self.chance = 0
            self.superposition = False
            qbit, wbit = QuiteBit(chance, True, 1), QuiteBit(chance, True, 0)
        return qbit, wbit

    def put_into_superposition(self):
        self.superposition = True
        self.value = None

    def get_value(self):
        if self.superposition:
            return None
        else:
            return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)
