from ..interfaces import *
from ...domain.models import *
from ...domain.services import *


__all__ = ['SampleGameQueryService']


class SampleGameQueryService(IQueryService):
    def game1(self) -> Team:
        game = GameService(
            [Monster.from_name('Skeleton', is_leader=i == 0)
                for i in range(10)],
            [Monster.from_name('Skeleton', is_leader=i == 0)
                for i in range(10)]
        )
        return game.play()
