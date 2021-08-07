import collections
import random
from typing import Iterable, Optional
from .models import *


__all__ = [
    'MonsterAttackService',
    'MonsterQueueService',
    'GameService',
    'MonsterTeamService'
]


class MonsterAttackService:
    __DAMAGE_TABLE = {
        Attack.SLASH:  (2, 0),
        Attack.SHOOT:  (1, 2),
        Attack.CRUSH:  (2, 0),
        Attack.BREATH: (1, 1)
    }

    def __init__(self, armor_block: float=0.8, leader_coverage: float=2.0):
        self.rng = random.Random()
        self.armor_block = armor_block
        self.leader_coverage = leader_coverage

    def __armor_test(self, defense: Defense) -> bool:
        return self.rng.random() < self.armor_block \
            if defense & Defense.ARMOR else False

    def __damage(self, attacker: Monster, defender: Monster) -> int:
        dmg_g, dmg_a = self.__DAMAGE_TABLE[attacker.attack]
        if attacker.has_antiair:
            if dmg_a == 0:
                dmg_a = dmg_g
        dmg = dmg_a if defender.is_flying else dmg_g
        if attacker.attack is Attack.BREATH and defender.defense & Defense.RESIST:
            dmg = 0
        elif not attacker.has_piercing and defender.has_armor:
            dmg = max(dmg - self.__armor_test(defender.defense), 0)
        return dmg

    def __target(self, attacker: Monster,
        defenders: Iterable[Monster]) -> Iterable[Monster]:
        if attacker.attack == Attack.BREATH:
            return defenders
        return random.choices(
            defenders,
            weights=[self.leader_coverage if d.is_leader else 1.0
                for d in defenders],
            k=1
        )

    def attack(self, attacker: Monster, defenders: Iterable[Monster]) -> None:
        for defender in self.__target(attacker, defenders):
            damage = self.__damage(attacker, defender)
            defender.hp = max(defender.hp - damage, 0)


class MonsterQueueData:
    def __init__(self, team: Team, monster: Monster, has_turn: bool=False):
        self.team = team
        self.monster = monster
        self.has_turn = has_turn

    def __eq__(self, other: 'MonsterQueueData') -> bool:
        return self.monster == other.monster


class MonsterQueueService:
    def __init__(self):
        self.__queue = collections.deque()

    @property
    def is_empty(self) -> bool:
        return not self.__queue

    def monsters(self, team: Optional[Team]=None) -> Iterable[MonsterQueueData]:
        return [x for x in self.__queue if x.team == team or team is None]

    def winner(self) -> Optional[Team]:
        if len(self.monsters(Team.RED)) == 0:
            return Team.BLUE
        if len(self.monsters(Team.BLUE)) == 0:
            return Team.RED
        return None

    def push(self, data: MonsterQueueData) -> None:
        if data in self.__queue:
            return
        elif data.monster.is_dead:
            return
        self.__queue.append(data)

    def pop(self) -> Optional[MonsterQueueData]:
        if self.is_empty:
            return None
        if not self.__queue[0].has_turn:
            monsters = self.monsters()
            for m in monsters:
                m.has_turn = True
            random.shuffle(monsters)
            self.__queue = collections.deque(monsters)
        m = self.__queue.popleft()
        m.has_turn = False
        self.__queue.append(m)
        return m

    def purge(self) -> None:
        monsters = self.monsters()
        self.__queue.clear()
        for m in monsters:
            self.push(m)


class GameService:
    def __init__(self, team_red: Iterable[Monster], team_blue: Iterable[Monster]):
        if sum(m.is_leader for m in team_red) != 1:
            raise ValueError('no leader exists')
        if sum(m.is_leader for m in team_blue) != 1:
            raise ValueError('no leader exists')
        if sum(m.sp for m in team_red) > 10:
            raise ValueError('total sp cannot be more than 10')
        if sum(m.sp for m in team_blue) > 10:
            raise ValueError('total sp cannot be more than 10')
        self.attack_service = MonsterAttackService()
        self.queue = MonsterQueueService()
        for monster in team_red:
            self.queue.push(MonsterQueueData(Team.RED, monster))
        for monster in team_blue:
            self.queue.push(MonsterQueueData(Team.BLUE, monster))

    def play1(self) -> Team:
        attacker = self.queue.pop()
        defenders = [m.monster for m in self.queue.monsters(attacker.team.opposite)]
        self.attack_service.attack(attacker.monster, defenders)
        self.queue.purge()
        return self.queue.winner()

    def play(self) -> Team:
        while True:
            team = self.play1()
            if team is not None:
                return team


class MonsterTeamService:
    class Node:
        def __init__(self, index, sp, parent=None, is_leader=False):
            self.index = index
            self.sp = sp
            self.parent = parent
            self.children = []
            self.is_leader = is_leader

        @property
        def is_leaf(self) -> bool:
            return not self.children

        @property
        def signature(self) -> Iterable[int]:
            s = []
            n = self
            while n:
                s.insert(0, n.index)
                n = n.parent
            return s

    def sp10_combinations(self) -> Iterable[Iterable[int]]:
        cost = [(i, m.sp) for i, m in enumerate(MonsterDataList)]
        root = self.Node(None, 10)
        result = []
        for i, sp in cost:
            if root.sp - sp >= 0:
                n = self.Node(i, root.sp - sp, None, is_leader=True)
                root.children.append(n)
        q = collections.deque(root.children)
        while q:
            node = q.popleft()
            samples = cost if node.is_leader else cost[node.index:]
            for i, sp in samples:
                if node.sp - sp >= 0:
                    node.children.append(self.Node(i, node.sp - sp, node))
            if node.is_leaf and node.sp == 0:
                result.append(node.signature)
            else:
                q.extend(node.children)
        return sorted(result)
