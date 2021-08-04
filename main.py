from lomr1.genetics.services.gene import GeneQueryService
from lomr1.base import *
from lomr1.genetics import *


def on_begin(n, genes):
    print(n)


def on_end(n, genes):
    for gene in genes[:5]:
        print(gene.build_team())


GeneQueryService().get(
    generations=1000,
    samples=3000,
    on_begin=on_begin,
    on_end=on_end
)
