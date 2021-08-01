from lomr1.genetics.services.gene import GeneQueryService
from lomr1.base import *
from lomr1.genetics import *


def on_begin(n, genes):
    print(n)


def on_end(n, genes):
    for gene in genes[:5]:
        print(gene)


GeneQueryService().get(
    on_begin=on_begin,
    on_end=on_end
)
