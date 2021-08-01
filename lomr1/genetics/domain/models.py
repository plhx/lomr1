import random
from typing import Iterable
from ...base import *


__all__ = ['MonsterGene']


class MonsterGene:
    def __init__(self, value: Iterable[int]):
        self.value = value

    def __repr__(self) -> str:
        return '<{}: {}>'.format(
            self.__class__.__name__,
            ''.join('012345678-'[x] for x in self.value)
        )

    @classmethod
    def random(cls, n=10) -> 'MonsterGene':
        while True:
            g = random.choices(range(10), k=n)
            g += [9] * (10 - len(g))
            r = cls(g)
            if r.is_valid():
                return r

    def is_valid(self) -> bool:
        sp = 0
        for x in self.value:
            if x in range(len(MonsterDataList)):
                sp += Monster.from_index(x).sp
        return 1 <= sp <= 10

    def mutate(self) -> 'MonsterGene':
        while True:
            g = self.value.copy()
            g[random.randrange(10)] = random.randrange(10)
            r = self.__class__(g)
            if r.is_valid():
                return r

    def cross(self, other: 'MonsterGene') -> 'MonsterGene':
        while True:
            g = [a if random.random() < 0.5 else b
                for a, b in zip(self.value, other.value)]
            r = self.__class__(g)
            if r.is_valid():
                return r

    def build_team(self) -> Iterable[Monster]:
        g = [x for x in self.value if x < 9]
        return [Monster.from_index(x, is_leader=i == 0)
            for i, x in enumerate(g)]
