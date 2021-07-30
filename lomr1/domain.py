import collections
import random
from typing import Iterable, Optional
from .models import *


__all__ = ['MonsterAttackService', 'MonsterQueueService', 'GameService']


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

    def __damage(self, attacker: IMonster, defender: IMonster) -> int:
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

    def __target(self, attacker: IMonster,
        defenders: Iterable[IMonster]) -> Iterable[IMonster]:
        if attacker.attack == Attack.BREATH:
            return defenders
        return random.choices(
            defenders,
            weights=[self.leader_coverage if d.is_leader else 1.0
                for d in defenders],
            k=1
        )

    def attack(self, attacker: IMonster, defenders: Iterable[IMonster]) -> None:
        for defender in self.__target(attacker, defenders):
            damage = self.__damage(attacker, defender)
            defender.hp = max(defender.hp - damage, 0)


class MonsterQueueService:
    def __init__(self, team: Team, monsters: Iterable[IMonster]=()):
        self.team = team
        self.__queue = collections.deque(monsters)

    def push(self, monster: IMonster) -> None:
        if monster in self.__queue:
            return
        elif monster.is_dead:
            return
        self.__queue.append(monster)

    def pop(self) -> Optional[IMonster]:
        return None if self.is_empty else self.__queue.popleft()

    def purge(self) -> None:
        monsters = self.monsters
        self.__queue.clear()
        for monster in monsters:
            self.push(monster)

    @property
    def is_empty(self) -> bool:
        return not self.__queue

    @property
    def monsters(self) -> Iterable[IMonster]:
        return tuple(self.__queue)


class GameService:
    def __init__(self, team_red: Iterable[IMonster], team_blue: Iterable[IMonster]):
        if sum(m.is_leader for m in team_red) != 1:
            raise ValueError('no leader exists')
        if sum(m.is_leader for m in team_blue) != 1:
            raise ValueError('no leader exists')
        if sum(m.sp for m in team_red) > 10:
            raise ValueError('total sp cannot be more than 10')
        if sum(m.sp for m in team_blue) > 10:
            raise ValueError('total sp cannot be more than 10')
        self.rng = random.Random()
        self.attack_service = MonsterAttackService()
        teams = [
            MonsterQueueService(Team.RED, team_red),
            MonsterQueueService(Team.BLUE, team_blue)
        ]
        self.rng.shuffle(teams)
        self.attackers, self.defenders = teams

    def play1(self) -> Team:
        attacker = self.attackers.pop()
        self.attack_service.attack(attacker, self.defenders.monsters)
        self.defenders.purge()
        self.attackers.push(attacker)
        if self.defenders.is_empty:
            return self.attackers.team
        self.attackers, self.defenders = self.defenders, self.attackers

    def play(self) -> Team:
        while True:
            team = self.play1()
            if team is not None:
                return team
