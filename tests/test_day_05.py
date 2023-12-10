from textwrap import dedent

import pytest

from solutions.day_05 import (
    follow_one_p1,
    follow_p1,
    follow_one_p2,
    find_changeovers,
    find_all_changeovers,
    parse_line_1_p1,
    parse_line_1_p2,
    parse_lines,
    parse_p1,
    parse_p2,
    solve_p1,
    solve_p2,
    Category,
)


@pytest.fixture
def data():
    return dedent(
        """\
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """
    )


@pytest.fixture
def seeds_p1():
    return [79, 14, 55, 13]


@pytest.fixture
def seeds_p2():
    return [range(79, 79 + 14), range(55, 55 + 13)]


@pytest.fixture
def parsed_maps():
    return {
        (Category.SEED, Category.SOIL): [
            (range(98, 98 + 2), range(50, 50 + 2)),
            (range(50, 50 + 48), range(52, 52 + 48)),
        ],
        (Category.SOIL, Category.FERTILIZER): [
            (range(15, 15 + 37), range(0, 0 + 37)),
            (range(52, 52 + 2), range(37, 37 + 2)),
            (range(0, 0 + 15), range(39, 39 + 15)),
        ],
        (Category.FERTILIZER, Category.WATER): [
            (range(53, 53 + 8), range(49, 49 + 8)),
            (range(11, 11 + 42), range(0, 0 + 42)),
            (range(0, 0 + 7), range(42, 42 + 7)),
            (range(7, 7 + 4), range(57, 57 + 4)),
        ],
        (Category.WATER, Category.LIGHT): [
            (range(18, 18 + 7), range(88, 88 + 7)),
            (range(25, 25 + 70), range(18, 18 + 70)),
        ],
        (Category.LIGHT, Category.TEMPERATURE): [
            (range(77, 77 + 23), range(45, 45 + 23)),
            (range(45, 45 + 19), range(81, 81 + 19)),
            (range(64, 64 + 13), range(68, 68 + 13)),
        ],
        (Category.TEMPERATURE, Category.HUMIDITY): [
            (range(69, 69 + 1), range(0, 0 + 1)),
            (range(0, 0 + 69), range(1, 1 + 69)),
        ],
        (Category.HUMIDITY, Category.LOCATION): [
            (range(56, 56 + 37), range(60, 60 + 37)),
            (range(93, 93 + 4), range(56, 56 + 4)),
        ],
    }


def test_parse_p1(data, seeds_p1, parsed_maps):
    assert parse_p1(data) == (seeds_p1, parsed_maps)


def test_parse_line_1_p1(seeds_p1):
    assert parse_line_1_p1("seeds: 79 14 55 13") == seeds_p1


def test_parse_p2(data, seeds_p2, parsed_maps):
    seeds, maps = parse_p2(data)
    assert list(seeds) == seeds_p2
    assert maps == parsed_maps


def test_parse_line_1_p2(seeds_p2):
    assert list(parse_line_1_p2("seeds: 79 14 55 13")) == seeds_p2


def test_parse_lines(data, parsed_maps):
    assert parse_lines(data.splitlines()[1:]) == parsed_maps


@pytest.mark.parametrize(
    ["source", "expected_dest"],
    [
        (98, 50),
        (99, 51),
        (53, 55),
        (10, 10),
    ],
)
def test_follow_one_p1(source, expected_dest, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert follow_one_p1(source, mapping) == expected_dest


@pytest.mark.parametrize(
    ["sources", "expected_dests"],
    [
        (range(98, 98 + 2), range(50, 50 + 2)),
        (range(50, 50 + 48), range(52, 52 + 48)),
    ],
)
def test_follow_one_p2(sources, expected_dests, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert follow_one_p2(sources, mapping) == expected_dests


@pytest.mark.parametrize(
    ["seed", "expected_location"],
    [
        (79, 82),
        (14, 43),
        (55, 86),
        (13, 35),
    ],
)
def test_follow_p1(seed, expected_location, parsed_maps):
    assert follow_p1(seed, parsed_maps) == expected_location


@pytest.mark.parametrize(
    ["starting_set", "mapping", "expected"],
    [
        (
            set(),
            [
                (range(98, 98 + 2), range(50, 50 + 2)),
                (range(50, 50 + 48), range(52, 52 + 48)),
            ],
            {0, 50, 98, 100},
        )
    ],
)
def test_find_changeovers(starting_set, mapping, expected):
    assert find_changeovers(starting_set, mapping) == expected


def test_find_all_changeovers(parsed_maps):
    expected = {
        0,
        22,
        26,
        44,
        50,
        52,
        54,
        59,
        62,
        66,
        69,
        70,
        71,
        82,
        92,
        93,
        98,
        99,
        100,
    }
    assert find_all_changeovers(parsed_maps) == expected


def test_solve_p1(data):
    assert solve_p1(data) == 35


def test_solve_p2(data):
    assert solve_p2(data) == 46
