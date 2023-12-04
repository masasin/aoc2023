# %%
from dotenv import load_dotenv

load_dotenv()

from aocd import data
from scipy.ndimage import convolve
import numpy as np


def adjacent_number_coords(grid):
    grid = np.pad(grid, pad_width=1, mode="constant", constant_values=".")
    num_mask = np.char.isdigit(grid)
    sym_mask = (grid != ".") & ~num_mask
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    convolved_sym_mask = convolve(sym_mask.astype(int), kernel, mode="constant", cval=0)
    adjacent_number_mask = (convolved_sym_mask > 0) & num_mask
    return np.argwhere(adjacent_number_mask) - np.array([1, 1])


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


def extract_contiguous_number(row, col, grid):
    number = ""
    num_mask = np.char.isdigit(grid)
    i = col
    while i >= 0 and num_mask[row, i]:
        number = grid[row, i] + number
        i -= 1

    i = col + 1
    while i < len(grid[row]) and num_mask[row, i]:
        number += grid[row, i]
        i += 1

    return int(number)


def extract_numbers(coords, grid):
    for row, col in coords:
        yield extract_contiguous_number(row, col, grid)


def solve_p1(grid):
    unique_contiguous_numbers = extract_numbers(
        drop_contiguous_points(adjacent_number_coords(grid)), grid
    )
    return sum(unique_contiguous_numbers)


if __name__ == "__main__":
    grid = np.array(list(map(list, data.splitlines())))
    answer_p1 = solve_p1(grid)
    print(answer_p1)
