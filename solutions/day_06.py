import math
import re

from dotenv import load_dotenv

load_dotenv()

from aocd import data, submit


def parse_p1(data: str) -> tuple[list[int], list[int]]:
    times_str, distances_str = data.splitlines()
    times = [int(x) for x in re.findall(r"\d+", times_str)]
    distances = [int(x) for x in re.findall(r"\d+", distances_str)]
    return zip(times, distances)


def parse_p2(data: str) -> tuple[int, int]:
    time_str, distance_str = data.splitlines()
    total_time = int("".join(x for x in re.findall(r"\d+", time_str)))
    distance = int("".join(x for x in re.findall(r"\d+", distance_str)))
    return total_time, distance


def roots(total_time: int, record: int) -> tuple[float, float]:
    disc_root = math.sqrt(total_time**2 - 4 * record)
    return (total_time - disc_root) / 2, (total_time + disc_root) / 2


def ways_to_win(total_time: int, record: int) -> int:
    lower, upper = roots(total_time, record)
    min_score = math.ceil(lower) if int(lower) != lower else lower + 1
    max_score = math.floor(upper) if int(upper) != upper else upper - 1
    return max_score - min_score + 1


def solve_p1(data: str) -> int:
    return math.prod(
        ways_to_win(total_time, record) for total_time, record in parse_p1(data)
    )


def solve_p2(data: str) -> int:
    total_time, record = parse_p2(data)
    return ways_to_win(total_time, record)


if __name__ == "__main__":
    submit(solve_p1(data), part=1)
    submit(solve_p2(data), part=2)
