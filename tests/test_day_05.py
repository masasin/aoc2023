from textwrap import dedent

import pytest

from solutions.day_05 import (
    changeovers_to_mappings,
    compose_changeovers,
    dedup_changeovers,
    follow_from_changeovers,
    follow_one,
    follow_p1,
    delta_mappings,
    find_changeovers,
    find_all_changeovers,
    invert_changeovers,
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
def test_follow_down(source, expected_dest, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert follow_one(source, mapping) == expected_dest


@pytest.mark.parametrize(
    ["dest", "expected_source"],
    [
        (50, 98),
        (51, 99),
        (55, 53),
        (10, 10),
    ],
)
def test_follow_up(dest, expected_source, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert follow_one(dest, mapping, reverse=True) == expected_source


@pytest.mark.parametrize(
    ["source", "dest"],
    [
        (98, 50),
        (99, 51),
        (53, 55),
        (10, 10),
        (110, 110),
    ],
)
def test_follow_from_changeovers(source, dest):
    changeovers = {0: 0, 50: 2, 98: -48, 100: 0}
    assert follow_from_changeovers(source, changeovers) == dest
    assert follow_from_changeovers(dest, changeovers, reverse=True) == source


@pytest.mark.parametrize(
    ["original", "expected"],
    [
        (
            {0: 0, 50: 2, 98: -48, 100: 0},
            {0: 0, 50: 48, 52: -2, 100: 0},
        ),
        (
            {0: 39, 15: -15, 50: -13, 52: 2, 98: -63, 100: 0},
            {0: 15, 35: 63, 37: 13, 39: -39, 54: -2, 100: 0},
        ),
    ],
)
def test_invert_changeovers(original, expected):
    changeovers = {0: 0, 50: 2, 98: -48, 100: 0}
    assert invert_changeovers(changeovers) == {0: 0, 50: 48, 52: -2, 100: 0}


def test_changeovers_to_mappings():
    changeovers = {0: 0, 50: 2, 98: -48, 100: 0}
    assert set(changeovers_to_mappings(changeovers)) == {
        (range(50, 98), range(52, 100)),
        (range(98, 100), range(50, 52)),
    }


@pytest.mark.parametrize(
    ["dest", "expected_source"],
    [
        (50, 98),
        (51, 99),
        (55, 53),
        (10, 10),
    ],
)
def test_follow_up(dest, expected_source, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert follow_one(dest, mapping, reverse=True) == expected_source


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
    ["source", "expected_delta"],
    [
        (98, 50 - 98),
        (50, 52 - 50),
    ],
)
def test_delta(source, expected_delta, parsed_maps):
    mapping = parsed_maps[(Category.SEED, Category.SOIL)]
    assert delta_mappings(source, mapping) == expected_delta


@pytest.mark.parametrize(
    ["target_categories", "expected"],
    [
        (
            (Category.SEED, Category.SOIL),
            {0: 0, 50: 2, 98: -48, 100: 0},
        ),
        (
            (Category.SOIL, Category.FERTILIZER),
            {0: 39, 15: -15, 54: 0},
        ),
        (
            (Category.FERTILIZER, Category.WATER),
            {0: 42, 7: 50, 11: -11, 53: -4, 61: 0},
        ),
    ],
)
def test_find_changeovers(target_categories, expected, parsed_maps):
    assert find_changeovers(parsed_maps[target_categories]) == expected


def test_dedup_changeovers():
    changeovers = {0: 39, 15: -15, 52: -15, 54: 0}
    assert dedup_changeovers(changeovers) == {0: 39, 15: -15, 54: 0}


def test_find_all_changeovers(parsed_maps):
    expected = [
        {0: 0, 50: 2, 98: -48, 100: 0},
        {0: 39, 15: -15, 54: 0},
        {0: 42, 7: 50, 11: -11, 53: -4, 61: 0},
        {0: 0, 18: 70, 25: -7, 95: 0},
        {0: 0, 45: 36, 64: 4, 77: -32, 100: 0},
        {0: 1, 69: -69, 70: 0},
        {0: 0, 56: 4, 93: -37, 97: 0},
    ]
    assert list(find_all_changeovers(parsed_maps)) == expected


@pytest.mark.parametrize(
    ["changeovers", "expected"],
    [
        (
            [
                {0: 0, 50: 2, 98: -48, 100: 0},
                {0: 39, 15: -15, 52: -15, 54: 0},
            ],
            {0: 39, 15: -15, 50: -13, 52: 2, 98: -63, 100: 0},
        ),
        (
            [
                {0: 39, 15: -15, 50: -13, 52: 2, 98: -63, 100: 0},
                {0: 42, 7: 50, 11: -11, 53: -4, 61: 0},
            ],
            {
                0: 28,
                14: 35,
                15: 27,
                22: 35,
                26: -26,
                50: -24,
                52: -2,
                59: 2,
                98: -74,
                100: 0,
            },
        ),
        (
            [
                {0: 0, 50: 2, 98: -48, 100: 0},
                {0: 39, 15: -15, 52: -15, 54: 0},
                {0: 42, 7: 50, 11: -11, 53: -4, 61: 0},
            ],
            {
                0: 28,
                14: 35,
                15: 27,
                22: 35,
                26: -26,
                50: -24,
                52: -2,
                59: 2,
                98: -74,
                100: 0,
            },
        ),
    ],
)
def test_compose_changeovers(changeovers, expected):
    assert compose_changeovers(*changeovers) == expected


def test_solve_p1(data):
    assert solve_p1(data) == 35


def test_solve_p2(data):
    assert solve_p2(data) == 46
