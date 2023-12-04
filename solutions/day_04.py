from dotenv import load_dotenv

load_dotenv()

from aocd import data, submit


def parse_line(line):
    _, cards = line.split(": ")
    winning, yours = cards.split(" | ")
    return set(map(int, winning.split())), set(map(int, yours.split()))


def score_p1(winning, yours):
    return int(2 ** (len(winning & yours) - 1))


def solve_p1(data):
    return sum(score_p1(*parse_line(line)) for line in data.splitlines())


submit(solve_p1(data))
