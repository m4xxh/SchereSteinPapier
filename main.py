import argparse
import re
import os
from collections.abc import Collection
from random import choice

from functools import partial


class Rules:
    def __init__(
        self,
        distinct_objects: Collection[str],
        ruleset: dict[tuple[str, str], str],
    ):
        num_objects: int = len(distinct_objects)
        assert (num_objects - 1) * num_objects / 2 == len(
            ruleset
        ), "Not enough rules to cover object relations"
        self.distinct_objects: Collection = distinct_objects
        self.ruleset: dict[tuple[str, str], str] = ruleset

    @classmethod
    def parse(cls, path: str | os.PathLike):
        with open(path, "r") as file:
            rules: list[str] = file.read().splitlines()
        ruleset: list[tuple[str, str, str]] = [
            matches
            for line in rules
            if len(matches := tuple(re.findall(r"(\w+)", line))) == 3
        ]
        ruleset_dict: dict[tuple[str, str], str] = {
            (object1, object2): mechanism
            for object1, mechanism, object2 in ruleset
        }
        distinct_objects: list[str] = list(
            set(object for rule in ruleset for object in rule[::2])
        )
        return cls(distinct_objects, ruleset_dict)


class HumanPlayer:
    def __init__(self, name: str = "Mensch"):
        self.name: str = name

    def play(self, objects):
        chosen_object = input(
            f"\n{'-'*80}\nWähle einen Gegenstand:\t{', '.join(objects)}\n"
        )
        if chosen_object in objects:
            print(f"Du hast {chosen_object} gewählt.")
            return chosen_object
        else:
            print("Diesen Gegenstand gibt es nicht!")
            return self.play(objects)


class ComputerPlayer:
    def __init__(self, name: str = "Computer"):
        self.name: str = name

    def play(self, objects):
        chosen_object = choice(objects)
        print(f"Der Computer hat {chosen_object} gewählt.")
        return chosen_object


class Player:
    def __init__(self, playerType: HumanPlayer | ComputerPlayer) -> None:
        self.score: int = 0
        self.playerType = playerType

    def increment_score(self) -> None:
        self.score += 1

    def get_score(self) -> int:
        return self.score

    def __repr__(self):
        return self.playerType.name

    def __call__(self, objects, *args, **kwds):
        return self.playerType.play(objects=objects)


class Game:
    def __init__(
        self, player1: Player, player2: Player, rules: Rules, winningCondition
    ):
        self.player1 = player1
        self.player2 = player2
        self.rules = rules
        self.winningCondition = winningCondition

    def print_scores(self):
        print(
            f"{self.player1}: {self.player1.get_score()} - {self.player2.get_score()} :{self.player2}"
        )

    def scored(self, objects: tuple[str, str], player: Player):
        print(f"\n{objects[0]} {self.rules.ruleset.get(objects)} {objects[1]}")
        print(f"{player} erhält einen Punkt")
        player.increment_score()
        self.print_scores()

    def play(self):
        while not self.checkWinningCondition():
            player1_object: str = self.player1(self.rules.distinct_objects)
            player2_object: str = self.player2(self.rules.distinct_objects)
            if (
                objects := (player1_object, player2_object)
            ) in self.rules.ruleset:
                self.scored(objects, self.player1)
            elif (
                objects := (player2_object, player1_object)
            ) in self.rules.ruleset:
                self.scored(objects, self.player2)
            else:
                print("\nUnentschieden!\nNiemand bekommt Punkte\n")
        self.announce_winner()

    def announce_winner(self):
        winner = self.winningCondition(
            self.player1.get_score(), self.player2.get_score()
        )
        if all(winner):
            print("Beide haben gewonnen!")
        else:
            print(
                f"{[self.player1, self.player2][winner.index(True)]} hat gewonnen"
            )

    def checkWinningCondition(self) -> bool:
        return any(
            self.winningCondition(
                self.player1.get_score(), self.player2.get_score()
            )
        )


def win_condition_best_out_of(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    """Win Condtion"""
    win_condition: int = number // 2
    return (score_player1 > win_condition, score_player2 > win_condition)


def win_condition_number_wins(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    return (score_player1 > number, score_player2 > number)


def win_condition_number_games(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    score_sum: int = score_player1 + score_player2
    game_ends: bool = score_sum >= number
    score_winning: int = max(score_player1, score_player2)
    return (
        game_ends and (score_player1 == score_winning),
        game_ends and (score_player2 == score_winning),
    )


def main():
    game = Game(
        Player(HumanPlayer()),
        Player(ComputerPlayer()),
        Rules.parse(
            "./rules/extended.txt",
        ),
        partial(win_condition_best_out_of, 3),
    )
    game.play()


if __name__ == "__main__":
    main()
