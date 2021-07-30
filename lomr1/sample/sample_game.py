from ..domain import *
from ..models import *
from ..service import *


class SampleGameRequest(IServiceRequest):
    def __init__(self):
        self.team_red = [Skeleton for i in range(10)]
        self.team_blue = [Skeleton for i in range(10)]


class SampleGameResponse(IServiceResponse):
    def __init__(self, winner: Team):
        self.winner = winner


class SampleGameHandler(IServiceHandler):
    def handle(self, request: IRequest) -> IResponse:
        game = GameService(
            [x(is_leader=i == 0) for i, x in enumerate(request.team_red)],
            [x(is_leader=i == 0) for i, x in enumerate(request.team_blue)]
        )
        winner = game.play()
        return SampleGameResponse(winner)
