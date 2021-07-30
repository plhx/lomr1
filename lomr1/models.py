import abc
import enum
import dataclasses
from typing import Optional
import uuid


__all__ = [
    'Attack', 'Defense', 'IMonster',
    'Skeleton', 'Gnome', 'Hellhound', 'Falcon',
    'Lizardman', 'Elf', 'Ogre', 'Golem', 'Dragon',
    'Team'
]


class Attack(enum.IntFlag):
    SLASH = 1
    SHOOT = 2
    CRUSH = 4
    BREATH = 8


class Defense(enum.IntFlag):
    NONE = 0
    ARMOR = 1
    FLYING = 2
    RESIST = 4


@dataclasses.dataclass(init=True, repr=True)
class IMonsterData(metaclass=abc.ABCMeta):
    mid: int
    hp: int
    sp: int
    attack: Attack
    defense: Defense
    is_leader: bool

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0


class IMonster(IMonsterData):
    def __init__(self, mid: Optional[str], hp:int, sp: int,
        attack: Attack, defense: Defense, is_leader: bool=False):
        mid = mid or str(uuid.uuid4())
        super().__init__(
            str(uuid.uuid4()) if mid is None else mid,
            hp + bool(is_leader),
            sp,
            attack,
            defense,
            is_leader
        )

    def __eq__(self, other: 'IMonster') -> bool:
        return self.mid == other.mid

    @property
    def is_flying(self) -> bool:
        return bool(self.defense & Defense.FLYING)

    @property
    def has_armor(self) -> bool:
        return bool(self.defense & Defense.ARMOR)

    @property
    def has_antiair(self) -> bool:
        return bool(self.attack & (Attack.SHOOT | Attack.BREATH) \
            or self.defense & Defense.FLYING)

    @property
    def has_piercing(self) -> bool:
        return bool(self.attack & (Attack.CRUSH | Attack.BREATH))


class Skeleton(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 1, 1, Attack.SLASH, Defense.NONE, is_leader)


class Gnome(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 1, 1, Attack.SHOOT, Defense.NONE, is_leader)


class Hellhound(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 2, 2, Attack.SLASH, Defense.RESIST, is_leader)


class Falcon(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 2, 2, Attack.SLASH, Defense.FLYING, is_leader)


class Lizardman(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 2, 2, Attack.SLASH, Defense.ARMOR, is_leader)


class Elf(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 2, 2, Attack.SHOOT, Defense.ARMOR, is_leader)


class Ogre(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 4, 3, Attack.CRUSH, Defense.NONE, is_leader)


class Golem(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 4, 4, Attack.CRUSH, Defense.ARMOR, is_leader)


class Dragon(IMonster):
    def __init__(self, *, mid: str=None, is_leader=False):
        super().__init__(mid, 8, 6, Attack.BREATH, Defense.NONE, is_leader)


class Team(enum.IntFlag):
    RED = 1
    BLUE = 2
