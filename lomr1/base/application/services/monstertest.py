from ..interfaces import *
from ...domain.models import *
from ...domain.services import *


__all__ = ['MonsterTestQueryService']


class MonsterTestQueryService(IQueryService):
    r = [
        [0, 0, 0, 2, (0, 1), (0, 1), 2, (2, 3), 6], # Skeleton
        [0, 0, 1, 0, (1, 2), (1, 2), 3, (3, 4), 7], # Gnome
        [0, 0, 0, 2, (0, 1), (0, 1), 2, (2, 3), 6], # Hellhound
        [0, 0, 0, 0, (0, 1), (0, 1), 2, (2, 3), 6], # Falcon
        [0, 0, 0, 2, (0, 1), (0, 1), 2, (2, 3), 6], # Lizardman
        [0, 0, 1, 0, (1, 2), (1, 2), 3, (3, 4), 7], # Elf
        [0, 0, 0, 2,      0,      0, 2,      2, 6], # Ogre
        [0, 0, 0, 2,      0,      0, 2,      2, 6], # Golem
        [0, 0, 2, 1,      1,      1, 3,      3, 7], # Dragon
    ]

    def attack_test(self) -> None:
        s = MonsterAttackService()
        assert(len(MonsterDataList) == 9)
        for i, da in enumerate(MonsterDataList):
            for j, db in enumerate(MonsterDataList):
                a, b = Monster.from_data(da), Monster.from_data(db)
                s.attack(a, [b])
                n = self.r[i][j]
                if isinstance(n, int):
                    assert b.hp == n, '{} -> {}'.format(i, j, a, b)
                else:
                    assert b.hp in n, '{} -> {}'.format(i, j, a, b)
