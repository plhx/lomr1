from lomr1.genetics.services.gene import GeneQueryService
from lomr1.base import *
from lomr1.genetics import *


def on_begin(n, genes):
    print(n)


stats = {}


def on_gameend(n, winners):
    for w in winners:
        k = tuple(w.normalized().value)
        stats[k] = stats.get(k, 0) + 1
    occur = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (k, n) in enumerate(occur, start=1):
        print('{} ({} pts): {}'.format(i, n, MonsterGene(k).build_team()))


GeneQueryService().get(
    generations=1000,
    samples=3000,
    on_begin=on_begin,
    on_gameend=on_gameend
)
