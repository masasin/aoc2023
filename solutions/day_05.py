from collections import defaultdict
import enum
import itertools as it
from typing import Generator, Iterable

from dotenv import load_dotenv

load_dotenv()

from aocd import data, submit


class Category(enum.Enum):
    SEED = enum.auto()
    SOIL = enum.auto()
    FERTILIZER = enum.auto()
    WATER = enum.auto()
    LIGHT = enum.auto()
    TEMPERATURE = enum.auto()
    HUMIDITY = enum.auto()
    LOCATION = enum.auto()


MappingCategories = tuple[Category, Category]
MappingRanges = tuple[range, range]
Mappings = dict[MappingCategories, list[MappingRanges]]
Changeovers = dict[int, int]


def parse_p1(
    data: str,
) -> tuple[list[int], Mappings]:
    lines = data.splitlines()
    header = parse_line_1_p1(lines[0])
    mappings = parse_lines(lines[1:])
    return header, mappings


def parse_line_1_p1(line: str) -> list[int]:
    seeds = line.split(": ")[1]
    return list(map(int, seeds.split()))


def parse_p2(
    data: str,
) -> tuple[list[int], Mappings]:
    lines = data.splitlines()
    header = parse_line_1_p2(lines[0])
    mappings = parse_lines(lines[1:])
    return header, mappings


def parse_line_1_p2(line: str) -> Generator[range, None, None]:
    seeds = line.split(": ")[1].split()
    for start, size in zip(seeds[::2], seeds[1::2]):
        yield range(int(start), int(start) + int(size))


def parse_lines(lines: list[str]) -> Mappings:
    mappings = defaultdict(list)
    for line in lines:
        match line.split():
            case [categories, "map:"]:
                start, end = categories.split("-to-")
                current_categories = Category[start.upper()], Category[end.upper()]
            case [dest_start, source_start, range_length]:
                mappings[current_categories].append(
                    (
                        range(int(source_start), int(source_start) + int(range_length)),
                        range(int(dest_start), int(dest_start) + int(range_length)),
                    )
                )
    return mappings


def follow_one(
    source: int, mapping_ranges: MappingRanges, reverse: bool = False
) -> int:
    for ranges in mapping_ranges:
        source_range, dest_range = ranges[::-1] if reverse else ranges
        if source in source_range:
            return dest_range[source - source_range.start]
    return source


def follow_from_changeovers(
    source: int, changeovers: Changeovers, reverse: bool = False
) -> int:
    if reverse:
        return follow_from_changeovers(source, invert_changeovers(changeovers))
    keys = sorted(changeovers.keys())
    for start, end in zip(keys, keys[1:]):
        if start <= source < end:
            return source + changeovers[start]
    return source + changeovers[end]


def invert_changeovers(changeovers: Changeovers) -> Changeovers:
    mappings = changeovers_to_mappings(changeovers)
    inverted_mappings = [(dest, source) for source, dest in mappings]
    return find_changeovers(inverted_mappings)


def follow_p1(
    source: int,
    mappings: Mappings,
) -> int:
    for mapping in mappings.values():
        source = follow_one(source, mapping)
    return source


def delta_mappings(source: int, mapping_ranges: MappingRanges) -> int:
    return follow_one(source, mapping_ranges) - source


def dedup_changeovers(changeovers: Changeovers) -> Changeovers:
    deduped = {}
    last_delta = None
    for key in sorted(changeovers.keys()):
        if changeovers[key] != last_delta:
            deduped[key] = changeovers[key]
            last_delta = changeovers[key]
    return deduped


def find_changeovers(
    mapping: MappingRanges,
) -> Changeovers:
    changeovers = {0: 0}
    for source_range, _ in mapping:
        changeovers[source_range.start] = delta_mappings(source_range.start, mapping)
        changeovers[source_range.stop] = delta_mappings(source_range.stop, mapping)

    return dedup_changeovers(changeovers)


def changeovers_to_mappings(changeovers: Changeovers) -> MappingRanges:
    keys = sorted(changeovers.keys())
    for first, second in zip(keys, keys[1:]):
        source_range = range(first, second)
        dest_range = range(first + changeovers[first], second + changeovers[first])
        if source_range != dest_range:
            yield source_range, dest_range


def find_all_changeovers(mappings: Mappings) -> Generator[Changeovers, None, None]:
    for mapping in mappings.values():
        yield find_changeovers(mapping)


def compose_changeovers(*changeovers) -> Changeovers:
    if len(changeovers) > 2:
        return compose_changeovers(
            compose_changeovers(changeovers[0], changeovers[1]), *changeovers[2:]
        )

    first, second = changeovers
    changeovers = {}
    for source in sorted(first.keys()):
        dest = follow_from_changeovers(source, first)
        delta = follow_from_changeovers(dest, second) - source
        changeovers[source] = delta

    for key in sorted(second.keys()):
        source = follow_from_changeovers(key, first, reverse=True)
        dest = follow_from_changeovers(key, second)
        delta = dest - source
        changeovers[source] = delta

    return dedup_changeovers(changeovers)


def solve_p1(data: str) -> int:
    seeds, mappings = parse_p1(data)
    return min(follow_p1(seed, mappings) for seed in seeds)


def solve_p2(data: str) -> int:
    seed_ranges, mappings = parse_p2(data)
    changeovers = compose_changeovers(*find_all_changeovers(mappings))
    keys = sorted(changeovers.keys())
    minimum = float("inf")
    for seed_range in seed_ranges:
        keys_to_use = [key for key in keys if key in seed_range] + [seed_range.start]
        for key in keys_to_use:
            minimum = min(minimum, follow_from_changeovers(key, changeovers))
    return minimum


if __name__ == "__main__":
    submit(solve_p1(data), part=1)
    submit(solve_p2(data), part=2)
