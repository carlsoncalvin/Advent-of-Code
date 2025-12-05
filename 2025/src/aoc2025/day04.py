from pathlib import Path
import numpy as np
from numpy import ndarray, signedinteger

# I could probably use numba and parallelization, but for a first pass I'll just brute force

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> ndarray[tuple[int, int], np.dtype[bool]]:
    """Parses the input into a boolean grid of rolls and spaces."""
    lines = text.strip().splitlines()
    grid = np.empty((len(lines), len(lines[0])), dtype=bool)
    for i, line in enumerate(lines):
        row = np.array([0 if char == "." else 1 for char in line])
        grid[i, :] = row
    return grid

def get_window(grid: ndarray[tuple[int, int], np.dtype[bool|signedinteger]],
               row: int,
               col: int,
               n_rows: int,
               n_cols: int) -> ndarray[tuple[int, int], np.dtype[bool]]:
    """Returns a window centered around the given row and column, accounting for boundaries."""
    left = col - 1 if col > 0 else 0
    right = col + 2 if col < n_rows - 1 else None
    top = row - 1 if row > 0 else 0
    bottom = row + 2 if row < n_cols - 1 else None

    return grid[top:bottom, left:right]


def solve_part1(grid: ndarray[tuple[int, int], np.dtype[bool]]) -> int:
    """
    Slides a window along the grid and takes the sum of each window to find the total number of
    rolls. Skips spaces, and rolls in corners are always counted.
    """
    n_rows, n_cols = grid.shape
    top_or_bot = (0, n_rows-1)
    left_or_right = (0, n_cols-1)
    count = 0
    for row in range(n_rows):
        for col in range(n_cols):
            # skip if not a roll
            if not grid[row, col]:
                continue

            # corner case always true
            if row in top_or_bot and col in left_or_right:
                count += 1

            else:
                window = get_window(grid, row, col, n_rows, n_cols)
                window_sum = np.sum(window)
                if window_sum < 5:
                    count += 1

    return count

# for part 2 I'm going to do what I should have in the beginning and make a neighbor list that just
# gets updated. The plan is to id every spot in the grid sequentially to track the rolls.
# Okay the neighbor list is a dict not a list but whatever
def generate_nb_dict(grid: ndarray[tuple[int, int], np.dtype[bool]]):
    """
    Generates a dict of all rolls in the grid, keyed by a sequential roll id based on the roll's
    position in the grid. Dict values contain a list of all roll ids that are neighbors.
    """
    n_rows, n_cols = grid.shape
    nb_dict = {}
    id_grid = np.arange(n_rows * n_cols).reshape(n_rows, n_cols)

    # find all existing rolls and generate neighbor dict
    for row in range(n_rows):
        for col in range(n_cols):
            if grid[row, col]:
                spot_id = id_grid[row, col]
                nb_dict[spot_id] = []

    # reiterate through the entire grid and populate neighbor lists. there´s probably a more
    # efficient way but i can't think of it now. this only runs once so whatever
    for row in range(n_rows):
        for col in range(n_cols):
            if grid[row, col]:
                spot_id = id_grid[row, col]
                window = get_window(id_grid, row, col, n_rows, n_cols)
                all_neighbors = window.flatten().tolist()
                all_neighbors.remove(spot_id)
                nb_dict[spot_id] = [nb for nb in all_neighbors if nb in nb_dict.keys()]
    return nb_dict


def solve_part2(grid: ndarray[tuple[int, int], np.dtype[bool]]) -> int:
    """
    Iterates through the dict of neighbors and removes rolls that have less than 4 neighbors. When
    each roll is removed, only the affected neighbor lists are checked and updated.
    """
    n_rows, n_cols = grid.shape

    # generate dict of nb list and populate
    nb_dict = generate_nb_dict(grid)

    # this array computes all neighbors when added to a roll id
    nb_computer = np.array([-1 * (n_cols + 1), -1 * n_cols, -1 * (n_cols - 1),
                            -1,                                     1,
                            n_cols - 1,          n_cols,        n_cols + 1])

    # set counters
    count = None
    new_count = 0

    while count != new_count:
        rolls_to_pop = []
        count = new_count
        # loop through all rolls and check puzzle condition
        for roll, neighbors in nb_dict.items():
            # register roll to pop if puzzle condition is met
            if len(neighbors) < 4:
                rolls_to_pop.append(roll)

        # pop rolls from dict if registered and clean affected lists
        for roll in rolls_to_pop:
            nb_dict.pop(roll)
            ids_to_check = roll + nb_computer
            for id_to_check in ids_to_check:
                # nb_computer will return values not in the nb list near the boundaries. This try
                # except block makes it okay
                if id_to_check in nb_dict.keys():
                    try:
                        nb_dict[id_to_check].remove(roll)
                    except ValueError:
                        continue
            new_count += 1

    return count
# 8480 too low

def main() -> None:
    input_path = DATA_DIR / "day04.txt"
    text = input_path.read_text(encoding="utf-8")
    grid = parse_input(text)

    print("Day 4")
    print("Part 1:", solve_part1(grid))
    print("Part 2:", solve_part2(grid))


if __name__ == "__main__":
    main()
