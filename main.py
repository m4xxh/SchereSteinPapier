import argparse
import re
import os
from collections.abc import Callable, Collection
from random import choice
from functools import partial
from typing import Self


class Rules:
    def __init__(
        self,
        distinct_objects: Collection[str],
        ruleset: dict[tuple[str, str], str],
    ) -> None:
        """Definiert die Regeln, welche das Spiel befolgen soll

        Args:
            distinct_objects (Collection[str]): Spileobjekte,
                z.B. Schere, Stein, oder Papier
            ruleset (dict[tuple[str, str], str]): Die Regeln, welche beschreiben
                welches Objekt welches schlägt
        """
        num_objects: int = len(distinct_objects)
        assert (num_objects - 1) * num_objects / 2 == len(
            ruleset
        ), "Nicht genug Regeln, um alle Objektbeziehungen abzudecken"
        self.distinct_objects: Collection = distinct_objects
        self.ruleset: dict[tuple[str, str], str] = ruleset

    @classmethod
    def parse(cls, path: str | os.PathLike) -> Self:
        """Liest eine Regeldatei und erstellt das Regelobjekt zum spielen

        Args:
            path (str | os.PathLike): Dateipfad der Regeln

        Returns:
            Self: Ein Regelobjekt
        """
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


class Player:
    def __init__(self, name: str = "Unknown") -> None:
        """Basisklasse für Spieler:innen

        Args:
            name (str, optional): Name. Defaults to "Unknown".
        """
        self.score: int = 0
        self.name: str = name

    def increment_score(self, increment: int = 1) -> None:
        self.score += increment

    def get_score(self) -> int:
        return self.score

    def play(self, *args):
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.name

    def __call__(self, objects) -> str:
        return self.play(objects)


class HumanPlayer(Player):
    def __init__(self, name: str = "Mensch") -> None:
        """Ein Mensch, welcher Eingaben tätigen muss

        Args:
            name (str, optional): Name. Defaults to "Mensch".
        """
        super().__init__(name)

    def play(self, objects: list[str]) -> str:
        object_list: str = ", ".join(
            [f"{obj} [{idx}]" for idx, obj in enumerate(objects)]
        )
        chosen_object: str = input(f"Wähle einen Gegenstand:\t{object_list}\n")
        if chosen_object in objects:
            print(f"{self.name} hat {chosen_object} gewählt.")
            return chosen_object
        elif chosen_object.isdigit() and 0 <= (idx := int(chosen_object)) < len(
            objects
        ):
            return objects[idx]
        elif chosen_object == "exit":
            exit()
        else:
            print("Diesen Gegenstand gibt es nicht!")
            return self.play(objects)


class ComputerPlayer(Player):
    def __init__(self, name: str = "Computer") -> None:
        """Ein Computer, welcher "zufällig" spielt

        Args:
            name (str, optional): Name. Defaults to "Computer".
        """
        super().__init__(name)

    def play(self, objects: list[str]) -> str:
        chosen_object: str = choice(objects)
        print(f"{self.name} hat {chosen_object} gewählt.")
        return chosen_object


class Game:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        rules: Rules,
        winningCondition: Callable[[int, int], tuple[bool, bool]],
    ) -> None:
        """Ein Spiel zwischen zwei Spielenden

        Args:
            player1 (Player): Person 1 (Mensch/Computer)
            player2 (Player): Person 2 (Mensch/Computer)
            rules (Rules): Regelwerk
            winningCondition (Callable[[int, int], tuple[bool, bool]]): Funktion
                welche Gewinnbedingung prüft
        """
        self.player1: Player = player1
        self.player2: Player = player2
        self.rules: Rules = rules
        self.winningCondition: Callable[[int, int], tuple[bool, bool]] = (
            winningCondition
        )
        self.gameround: int = 1

    def print_scores(self) -> None:
        print(
            f"{self.player1}: {self.player1.get_score()}"
            + " - "
            + f"{self.player2.get_score()} :{self.player2}"
        )

    def scored(self, objects: tuple[str, str], player: Player) -> None:
        """Verteilt Punkte"""
        print(f"\n{objects[0]} {self.rules.ruleset.get(objects)} {objects[1]}")
        print(f"{player} erhält einen Punkt")
        player.increment_score()
        self.print_scores()

    def play(self) -> None:
        """Spielabwicklung"""
        while not self.checkWinningCondition():
            print(f"{'-'*80}")
            print(f"Runde {self.gameround}")
            print(f"{self.player1} ist dran")
            player1_object: str = self.player1.play(self.rules.distinct_objects)
            print(f"{self.player2} ist dran")
            player2_object: str = self.player2.play(self.rules.distinct_objects)
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
            self.gameround += 1
        self.announce_winner()

    def announce_winner(self) -> None:
        """Bekanntgabe wer gewonnen hat"""
        winner: tuple[bool, bool] = self.winningCondition(
            self.player1.get_score(), self.player2.get_score()
        )
        if all(winner):
            print("Beide haben gewonnen!")
        else:
            print(
                f"{[self.player1, self.player2][winner.index(True)]} hat gewonnen"
            )

    def checkWinningCondition(self) -> bool:
        """Überprüfung, ob schon jemand gewonnen hat"""
        return any(
            self.winningCondition(
                self.player1.get_score(), self.player2.get_score()
            )
        )


def win_condition_best_out_of(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    """Best-out-of-x Modell:
    Wer über die Hälfte der Punkte macht hat gewonnen
    """
    win_condition: int = number // 2
    return (score_player1 > win_condition, score_player2 > win_condition)


def win_condition_number_wins(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    """Wer eine bestimmte Anzahl an Rundengewinnen hat gewinnt das Spiel"""
    return (score_player1 > number, score_player2 > number)


def win_condition_number_games(
    number: int, score_player1: int, score_player2: int
) -> tuple[bool, bool]:
    """Eine bestimmte Anzahl an Spielen wird gespielt (Unentschieden möglich)"""
    score_sum: int = score_player1 + score_player2
    game_ends: bool = score_sum >= number
    score_winning: int = max(score_player1, score_player2)
    return (
        game_ends and (score_player1 == score_winning),
        game_ends and (score_player2 == score_winning),
    )


def main(args: argparse.Namespace) -> None:
    rules: Rules = Rules.parse(
        args.rules
        if args.rules
        else os.path.dirname(__file__)
        + ["/rules/classic.txt", "/rules/extended.txt"][args.extended]
    )
    if args.bestoutof:
        wincondition = partial(win_condition_best_out_of, args.bestoutof)
    elif args.numgames:
        wincondition = partial(win_condition_number_games, args.numgames)
    elif args.numberofwins:
        wincondition = partial(win_condition_number_wins, args.numberofwins)
    else:
        raise NotImplemented
    game = Game(HumanPlayer(), ComputerPlayer(), rules, wincondition)
    game.play()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Schere, Stein, Papier (& Erweiterungen)"
    )

    # Mutually exclusive group for extended/rules
    ruleset_group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group()
    )
    ruleset_group.add_argument(
        "--extended",
        action="store_true",
        help="Erweiterte Regeln mit Spock und Echse.",
    )
    ruleset_group.add_argument(
        "--rules", type=str, help="Dateipfad für eigen erstellte Regeln."
    )

    # Mutually exclusive group for game parameters
    wincondition_group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group(required=False)
    )
    wincondition_group.add_argument(
        "--bestoutof",
        type=int,
        default=3,
        help="Gewinnkondition: Mehrzahl der BESTOUTOF Spiele gewonnen (Standard=3).",
    )
    wincondition_group.add_argument(
        "--numgames", type=int, help="Das Spiel hört nach NUMGAMES Spielen auf."
    )
    wincondition_group.add_argument(
        "--numberofwins",
        type=int,
        help="Das Spiel hört nach NUMBEROFWINS Gewinnen auf.",
    )
    args: argparse.Namespace = parser.parse_args()
    main(args)
