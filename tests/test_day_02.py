from textwrap import dedent

import pytest

from solutions.day_02 import (
    Cubes,
    Game,
    parse,
    parse_draw,
    parse_draws,
    parse_game,
    power,
    solve_p1,
    solve_p2,
)


@pytest.fixture
def data():
    return dedent(
        """\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """
    )


@pytest.fixture
def max_cubes():
    return Cubes(red=12, green=13, blue=14)


@pytest.mark.parametrize(
    ["draw", "expected"],
    [
        (Cubes(red=4, blue=3), True),
        (Cubes(red=1, green=2, blue=20), False),
        (Cubes(green=2), True),
    ],
)
def test_cubes_possible(max_cubes, draw, expected):
    assert draw.possible(max_cubes) == expected


@pytest.mark.parametrize(
    ["game", "expected"],
    [
        (
            Game(
                id=1,
                draws=[Cubes(red=4, green=0, blue=3), Cubes(red=0, green=2, blue=0)],
            ),
            True,
        ),
        (
            Game(
                id=2,
                draws=[Cubes(red=1, green=2, blue=20), Cubes(red=0, green=2, blue=0)],
            ),
            False,
        ),
    ],
)
def test_games_possible(max_cubes, game, expected):
    assert game.possible(max_cubes) == expected


@pytest.mark.parametrize(
    ["draw_str", "expected"],
    [
        ("3 blue, 4 red", Cubes(red=4, green=0, blue=3)),
        ("1 red, 2 green, 6 blue", Cubes(red=1, green=2, blue=6)),
        ("2 green", Cubes(red=0, green=2, blue=0)),
    ],
)
def test_parse_draw(draw_str, expected):
    assert parse_draw(draw_str) == expected


def test_parse_draws():
    draws_str = "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    expected = [
        Cubes(red=4, blue=3),
        Cubes(red=1, green=2, blue=6),
        Cubes(green=2),
    ]
    assert list(parse_draws(draws_str)) == expected


def test_parse_game():
    game_str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    expected = Game(
        id=1,
        draws=[
            Cubes(red=4, blue=3),
            Cubes(red=1, green=2, blue=6),
            Cubes(green=2),
        ],
    )
    assert parse_game(game_str) == expected


def test_parse(data):
    assert list(parse(data)) == [
        Game(
            id=1,
            draws=[
                Cubes(red=4, blue=3),
                Cubes(red=1, green=2, blue=6),
                Cubes(green=2),
            ],
        ),
        Game(
            id=2,
            draws=[
                Cubes(blue=1, green=2),
                Cubes(green=3, blue=4, red=1),
                Cubes(blue=1, green=1),
            ],
        ),
        Game(
            id=3,
            draws=[
                Cubes(red=20, green=8, blue=6),
                Cubes(blue=5, red=4, green=13),
                Cubes(red=1, green=5),
            ],
        ),
        Game(
            id=4,
            draws=[
                Cubes(green=1, red=3, blue=6),
                Cubes(green=3, red=6),
                Cubes(blue=15, red=14, green=3),
            ],
        ),
        Game(
            id=5,
            draws=[
                Cubes(red=6, blue=1, green=3),
                Cubes(blue=2, red=1, green=2),
            ],
        ),
    ]


def test_solve_p1(data):
    assert solve_p1(parse(data)) == 8


@pytest.mark.parametrize(
    ["game", "expected"],
    [
        (
            Game(
                id=1,
                draws=[Cubes(red=4, green=0, blue=3), Cubes(red=0, green=2, blue=0)],
            ),
            Cubes(red=4, green=2, blue=3),
        ),
        (
            Game(
                id=2,
                draws=[Cubes(red=1, green=2, blue=20), Cubes(red=0, green=2, blue=0)],
            ),
            Cubes(red=1, green=2, blue=20),
        ),
    ],
)
def test_games_minimal_set(game, expected):
    assert game.minimal_set() == expected


@pytest.mark.parametrize(
    ["cubes", "expected"],
    [
        (Cubes(red=4, green=2, blue=3), 4 * 2 * 3),
        (Cubes(red=1, green=2, blue=20), 1 * 2 * 20),
    ],
)
def test_power(cubes, expected):
    assert power(cubes) == expected


def test_solve_p2(data):
    expected = 2286
    assert solve_p2(parse(data)) == expected
