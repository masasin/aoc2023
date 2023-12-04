from dotenv import load_dotenv

load_dotenv()

from aocd import data
from scipy.ndimage import convolve
import numpy as np


def sym_mask(grid):
    return (grid != ".") & ~np.char.isdigit(grid)


def gear_mask(grid):
    return grid == "*"


def adjacent_number_coords(mask):
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    convolved_mask = convolve(mask.astype(int), kernel, mode="constant", cval=0)
    adjacent_number_mask = (convolved_mask > 0) & num_mask
    return np.argwhere(adjacent_number_mask)


def drop_contiguous_points(coords):
    contiguous = np.all(
        np.logical_or(
            coords[1:] == coords[:-1],
            coords[1:] == coords[:-1] + 1,
        ),
        axis=1,
    )
    mask = np.append([True], np.logical_not(contiguous))
    return coords[mask]


def extract_contiguous_number(row, col):
    number = ""
    i = col
    while i >= 0 and num_mask[row, i]:
        number = grid[row, i] + number
        i -= 1

    i = col + 1
    while i < len(grid[row]) and num_mask[row, i]:
        number += grid[row, i]
        i += 1

    return int(number)


def extract_numbers(coords):
    for row, col in coords:
        yield extract_contiguous_number(row, col)


def solve_p1():
    mask = sym_mask(grid)
    adjacent_coords = drop_contiguous_points(adjacent_number_coords(mask))
    unique_contiguous_numbers = extract_numbers(adjacent_coords)
    return sum(unique_contiguous_numbers)


if __name__ == "__main__":
    grid = np.array(list(map(list, data.splitlines())))
    grid = np.pad(grid, pad_width=1, mode="constant", constant_values=".")
    num_mask = np.char.isdigit(grid)
    answer_p1 = solve_p1()
    print(answer_p1)

# %%
