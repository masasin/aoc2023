from textwrap import dedent

import pytest

from solutions.day_01 import (
    parse,
    extract_digits_p1,
    extract_digits_p2,
    extract_number,
    solve,
)


@pytest.fixture
def data_p1():
    return dedent(
        """\
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """
    )


@pytest.fixture
def data_p2():
    return dedent(
        """\
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        """
    )


@pytest.mark.parametrize(
    ["line", "expected"],
    [
        ("1abc2", [1, 2]),
        ("pqr3stu8vwx", [3, 8]),
        ("a1b2c3d4e5f", [1, 2, 3, 4, 5]),
        ("treb7uchet", [7]),
    ],
)
def test_extract_digits_p1(line, expected):
    assert list(extract_digits_p1(line)) == expected


@pytest.mark.parametrize(
    ["line", "expected"],
    [
        ("two1nine", [2, 1, 9]),
        ("eightwothree", [8, 2, 3]),
        ("abcone2threexyz", [1, 2, 3]),
        ("xtwone3four", [2, 1, 3, 4]),
        ("4nineeightseven2", [4, 9, 8, 7, 2]),
        ("zoneight234", [1, 8, 2, 3, 4]),
        ("7pqrstsixteen", [7, 6]),
    ],
)
def test_extract_digits_p2(line, expected):
    assert list(extract_digits_p2(line)) == expected


@pytest.mark.parametrize(
    ["digits", "expected"],
    [
        ([1, 2], 12),
        ([3, 8], 38),
        ([1, 2, 3, 4, 5], 15),
        ([7], 77),
    ],
)
def test_extract_number(digits, expected):
    assert extract_number(digits) == expected


def test_parse_p1(data_p1):
    expected = [12, 38, 15, 77]
    assert list(parse(data_p1, extract_digits_p1)) == expected


def test_parse_p2(data_p2):
    expected = [29, 83, 13, 24, 42, 14, 76]
    assert list(parse(data_p2, extract_digits_p2)) == expected


@pytest.mark.parametrize(
    ["numbers", "expected"],
    [
        ([12, 38, 15, 77], 142),
    ],
)
def test_solve(numbers, expected):
    assert solve(numbers) == expected
