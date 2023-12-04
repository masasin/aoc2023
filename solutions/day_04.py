from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

from aocd import data, submit


def parse_line(line):
    _, cards = line.split(": ")
    winning, yours = cards.split(" | ")
    return set(map(int, winning.split())), set(map(int, yours.split()))


def parse(data):
    yield from (parse_line(line) for line in data.splitlines())


def n_matches(winning, yours):
    return len(winning & yours)


def score_p1(winning, yours):
    return int(2 ** (n_matches(winning, yours) - 1))


def solve_p1(data):
    return sum(score_p1(*line) for line in parse(data))


def solve_p2(data):
    copies = defaultdict(lambda: 1)

    for i, (winning, yours) in enumerate(parse(data)):
        for j in range(i + 1, i + 1 + n_matches(winning, yours)):
            copies[j] += copies[i]
        copies[i]  # ensure current card is counted

    return sum(copies.values())


if __name__ == "__main__":
    submit(solve_p1(data), part=1)
    submit(solve_p2(data), part=2)
