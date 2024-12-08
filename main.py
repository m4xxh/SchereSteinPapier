import argparse
import re
import os
from collections.abc import Collection


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
    def __init__(self):
        pass


class ComputerPlayer:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
