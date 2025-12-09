from pathlib import Path
import numpy as np
from numpy import ndarray

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> ndarray[tuple[int, ...], np.dtype[int]]:
    return np.array([line.split(",") for line in text.strip().splitlines()], dtype=int)

def squared_distance(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2

def solve_part1(coords: ndarray[tuple[int, ...], np.dtype[int]]) -> int:
    # I know what I call top, bottom, etc. is actually inverted because the puzzle input has
    # (0,0) in the top left, not bottom right, but it doesn't change anything.

    # get the corners of the grid
    top_left = (max(coords[:, 0]), max(coords[:, 1]))
    top_right = (min(coords[:, 0]), max(coords[:, 1]))
    bottom_left = (max(coords[:, 0]), min(coords[:, 1]))
    bottom_right = (min(coords[:, 0]), min(coords[:, 1]))

    # find points closest to corners
    four_corners = np.array([top_left, top_right, bottom_left, bottom_right])
    four_closest = np.empty_like(four_corners, dtype=int)
    for i, corner in enumerate(four_corners):
        x1, y1 = corner
        closest = np.argmin(squared_distance(x1, y1, coords[:, 0], coords[:, 1]))
        four_closest[i] = coords[closest]

    # find max area amongst those points
    areas = set()
    for tile in four_closest:
        areas.update((np.abs(tile[0] - four_closest[:, 0]) + 1) *
                     (np.abs(tile[1] - four_closest[:, 1]) + 1))

    return max(areas)

# part 2
def compute_area(x1, y1, x2, y2):
    return (np.abs(x1 - x2) + 1) * (np.abs(y1 - y2) + 1)

def check_validity(x1, y1, x2, y2, bounds):
    """Checks if the sides of a rectangle intersect with any of the boundaries on the grid"""
    for i in range(len(bounds)):
        # account for wrap around
        if i == len(bounds) - 1:
            end = 0
        else:
            end = i + 1
        # sort boundary and rectangle ranges
        x_bound = sorted([bounds[i][0], bounds[end][0]])
        y_bound = sorted([bounds[i][1], bounds[end][1]])
        x_range = sorted([x1, x2])
        y_range = sorted([y1, y2])

        # account for boundaries that lie along a side. Skipping these lets me use >= and <= in the
        # collison logic
        if (x_range == x_bound and y_bound[0] == y_bound[1] and y_bound[0] in y_range) or\
            (y_range == y_bound and x_bound[0] == x_bound[1] and x_bound[0] in x_range):
            continue
        # check if the boundary is inside the rectangle
        rect_left_of_b = x_bound[1] <= x_range[0]
        rect_right_of_b = x_bound[0] >= x_range[1]
        rect_above_b = y_bound[1] <= y_range[0]
        rect_below_b = y_bound[0] >= y_range[1]
        # if all are false then the rectangle contains the boundary
        if sum([rect_left_of_b, rect_right_of_b, rect_above_b, rect_below_b]) == 0:
            return False
    return True

def solve_part2(coords: ndarray[tuple[int, ...], np.dtype[int]]) -> int:
    areas = set()
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            area = compute_area(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            # I know I don't have to check the entire polygon for every rectangle, but it doesn't
            # take that long, maybe a couple of minutes (less than 3), and I can't be bothered to
            # make it more efficient (it's 20:00, don't @ me)
            if check_validity(coords[i][0], coords[i][1], coords[j][0], coords[j][1], coords):
                areas.add(area)
    return max(areas)

def main() -> None:
    input_path = DATA_DIR / "day09.txt"
    text = input_path.read_text(encoding="utf-8")
    coords = parse_input(text)

    print("Day 9")
    print("Part 1:", solve_part1(coords))
    print("Part 2:", solve_part2(coords))

if __name__ == "__main__":
    main()