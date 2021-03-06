import random
from typing import Callable, Iterable
from ...base.application.interfaces import *
from ...base.domain.models import Team
from ...base.domain.services import GameService
from ..domain.models import *


class GeneQueryService(IQueryService):
    def get(self, generations=100, samples=1000, *, on_begin: Callable=None,
        on_end: Callable=None, on_gameend: Callable=None) -> Iterable[MonsterGene]:
        genes = [MonsterGene.random() for _ in range(samples)]
        for generation in range(generations):
            if callable(on_begin):
                on_begin(generation, genes)
            winners, losers = [], []
            while genes:
                a, b = genes.pop(), genes.pop()
                team = GameService(a.build_team(), b.build_team()).play()
                if team is Team.RED:
                    winners.append(a)
                    losers.append(b)
                else:
                    winners.append(b)
                    losers.append(a)
            if callable(on_gameend):
                on_gameend(generation, winners)
            genes = winners + random.sample(losers, k=(len(losers) // 2) & -1)
            children = []
            while len(children) < samples:
                a, b = random.sample(genes, k=2)
                r = random.random()
                if r < 0.01:
                    children.append(a.cross(b))
                elif r < 0.01 + 0.05:
                    children.append(a.mutate())
                else:
                    children.append(a)
            genes = children
            if callable(on_end):
                on_end(generation, genes)
        return genes
