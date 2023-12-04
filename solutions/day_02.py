from __future__ import annotations
from math import prod
from typing import Callable, Generator, Iterable
import re

from dotenv import load_dotenv

load_dotenv()

from aocd import submit, get_data
from pydantic import BaseModel, Field

data = get_data(day=2)


class Cubes(BaseModel):
    red: int = 0
    green: int = 0
    blue: int = 0

    def possible(self, max_cubes: Cubes) -> bool:
        return all(
            [
                self.red <= max_cubes.red,
                self.green <= max_cubes.green,
                self.blue <= max_cubes.blue,
            ]
        )


class Game(BaseModel):
    id: int
    draws: list[Cubes] = Field(default_factory=list)

    def possible(self, max_cubes: Cubes) -> bool:
        return all([draw.possible(max_cubes) for draw in self.draws])

    def minimal_set(self) -> Cubes:
        return Cubes(
            red=max(draw.red for draw in self.draws),
            green=max(draw.green for draw in self.draws),
            blue=max(draw.blue for draw in self.draws),
        )


def parse_draw(draw_str: str) -> Cubes:
    items = re.findall(r"(\d+) (\w+)", draw_str)
    return Cubes(**{color: int(count) for count, color in items})


def parse_draws(draws_str: str) -> Generator[Cubes, None, None]:
    yield from (parse_draw(draw_str) for draw_str in draws_str.split("; "))


def parse_game(game_str: str) -> Game:
    game_id_str, draws_str = game_str.split(": ")
    return Game(id=game_id_str.split()[-1], draws=parse_draws(draws_str))


def parse(data: str) -> Generator[Game, None, None]:
    yield from (parse_game(line) for line in data.splitlines())


def solve_p1(
    games: Iterable[Game], max_cubes: Cubes = Cubes(red=12, green=13, blue=14)
) -> int:
    return sum(game.id for game in games if game.possible(max_cubes))


def power(cubes: Cubes) -> int:
    return prod(cubes.dict().values())


def solve_p2(games: Iterable[Game]) -> int:
    return sum(power(game.minimal_set()) for game in games)


if __name__ == "__main__":
    games = list(parse(data))

    submit(solve_p1(games), part="a")
    submit(solve_p2(games), part="b")
