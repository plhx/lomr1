import dataclasses
import enum
from typing import Optional
import uuid


__all__ = [
    'Attack', 'Defense',
    'MonsterData', 'MonsterDataList', 'Monster',
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


@dataclasses.dataclass(init=True, repr=True, frozen=True)
class MonsterData:
    name: str
    sp: int
    hp: int
    attack: Attack
    defense: Defense


MonsterDataList = [
    MonsterData('Skeleton',  1, 1, Attack.SLASH,  Defense.NONE),
    MonsterData('Gnome',     1, 1, Attack.SHOOT,  Defense.NONE),
    MonsterData('Hellhound', 2, 2, Attack.SLASH,  Defense.RESIST),
    MonsterData('Falcon',    2, 2, Attack.SLASH,  Defense.FLYING),
    MonsterData('Lizardman', 2, 2, Attack.SLASH,  Defense.ARMOR),
    MonsterData('Elf',       2, 2, Attack.SHOOT,  Defense.ARMOR),
    MonsterData('Ogre',      3, 4, Attack.CRUSH,  Defense.NONE),
    MonsterData('Golem',     4, 4, Attack.CRUSH,  Defense.ARMOR),
    MonsterData('Dragon',    6, 8, Attack.BREATH, Defense.NONE)
]


class Monster:
    def __init__(self, name: str, sp: int, hp: int, attack: Attack,
        defense: Defense, *, is_leader: bool=False, mid: Optional[str]=None):
        self.name = name
        self.sp = sp
        self.hp = hp + bool(is_leader)
        self.attack = attack
        self.defense = defense
        self.is_leader = is_leader
        self.mid = mid or str(uuid.uuid4())

    @classmethod
    def from_index(cls, index: int,
        *, is_leader=False, mid: Optional[str]=None) -> 'Monster':
        return cls.from_data(
            MonsterDataList[index],
            is_leader=is_leader,
            mid=mid
        )

    @classmethod
    def from_name(cls, name: str,
        *, is_leader=False, mid: Optional[str]=None) -> 'Monster':
        for m in MonsterDataList:
            if m.name == name:
                return cls.from_data(m, is_leader=is_leader, mid=mid)
        raise ValueError('{} not found'.format(name))

    @classmethod
    def from_data(cls, data: MonsterData,
        *, is_leader=False, mid: Optional[str]=None) -> 'Monster':
        return cls(
            data.name, data.sp, data.hp, data.attack, data.defense,
            is_leader=is_leader,
            mid=mid
        )

    def __repr__(self) -> str:
        return '<{}: (hp: {})>'.format(self.name, self.hp)

    def __eq__(self, other: 'Monster') -> bool:
        return self.mid == other.mid

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0

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


class Team(enum.IntFlag):
    RED = 1
    BLUE = 2
