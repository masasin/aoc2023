from typing import Callable, Generator

from dotenv import load_dotenv

load_dotenv()

from aocd import data, submit


def extract_digits_p1(line: str) -> Generator[int, None, None]:
    yield from (int(char) for char in line if char.isdigit())


def extract_digits_p2(line: str) -> Generator[int, None, None]:
    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for i in range(len(line)):
        if line[i].isdigit():
            yield int(line[i])
        else:
            for word, num in number_words.items():
                if line[i:].startswith(word):
                    yield num
                    break


def extract_number(digits: list[int]) -> int:
    digits = list(digits)
    return int(f"{digits[0]}{digits[-1]}")


def parse(data: str, digit_extractor: Callable) -> Generator[int, None, None]:
    yield from (extract_number(digit_extractor(line)) for line in data.splitlines())


def solve(numbers) -> int:
    return sum(numbers)


if __name__ == "__main__":
    numbers_p1 = parse(data, extract_digits_p1)
    answer_p1 = solve(numbers_p1)
    submit(answer_p1)

    numbers_p2 = parse(data, extract_digits_p2)
    answer_p2 = solve(numbers_p2)
    submit(answer_p2)
