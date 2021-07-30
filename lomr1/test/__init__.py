from ..models import *
from ..domain import *


def run_test():
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
    s = MonsterAttackService()
    monsters = [
        Skeleton, Gnome, Hellhound, Falcon, Lizardman,
        Elf, Ogre, Golem, Dragon
    ]
    for i, ma in enumerate(monsters):
        for j, mb in enumerate(monsters):
            a, b = ma(), mb()
            s.attack(a, [b])
            n = r[i][j]
            if isinstance(n, int):
                assert b.hp == n, '({}, {}) {} -> {}'.format(i, j, a, b)
            else:
                assert b.hp in n, '({}, {}) {} -> {}'.format(i, j, a, b)
