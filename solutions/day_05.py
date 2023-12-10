from collections import defaultdict
import enum
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


def follow_one_p1(source: int, mapping_ranges: MappingRanges) -> int:
    for source_range, dest_range in mapping_ranges:
        if source in source_range:
            return dest_range[source - source_range.start]
    return source


def follow_one_p2(source_range: range, mapping_ranges: MappingRanges) -> range:
    return range(
        follow_one_p1(source_range.start, mapping_ranges),
        follow_one_p1(source_range.stop - 1, mapping_ranges) + 1,
    )


def follow_p1(
    source: int,
    mappings: Mappings,
) -> int:
    for mapping in mappings.values():
        source = follow_one_p1(source, mapping)
    return source


def find_all_changeovers(mappings: Mappings) -> set[int]:
    ...


def solve_p1(data: str) -> int:
    seeds, mappings = parse_p1(data)
    return min(follow_p1(seed, mappings) for seed in seeds)


def solve_p2(data: str) -> int:
    seeds, mappings = parse_p2(data)
    return min(
        follow_p1(seed, mappings)
        for seed in find_all_changeovers(mappings)
        if seed in seeds
    )


if __name__ == "__main__":
    submit(solve_p1(data), part=1)
    # submit(solve_p2(data), part=2)
