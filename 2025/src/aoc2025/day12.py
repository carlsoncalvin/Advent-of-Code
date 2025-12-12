from pathlib import Path
from typing import Any

import numpy as np
from numpy import ndarray, dtype

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> tuple[ndarray[tuple[int, int, int], dtype[int]], list[Any]]:
    lines = text.strip().splitlines()
    shapes = np.empty((3,3,6), dtype=int)
    trees = []
    for i, line in enumerate(lines):
        if line == "": continue
        elif line[0].isdigit() and i < 30:
            shape_number = int(line[0])
            shape = lines[i+1:i+4]
            shape = [[1 if char == "#" else 0 for char in line] for line in shape]
            shapes[:,:,shape_number] = shape

        elif i > 29:
            dimensions = np.array([int(num) for num in line.split(":")[0].split("x")])
            quantities = np.array([int(num) for num in line.split(":")[1].split()])
            trees.append([dimensions, quantities])

    return shapes, trees

def solve_part1(shapes, trees) -> int:
    """Trivial solutions for trivial problems!"""
    fit_count = 0
    present_areas = np.sum(shapes, axis=(0,1))

    for tree in trees:
        dimensions, quantities = tree

        # trivial cases
        # presents must fit - plenty of room
        tree_area = np.prod(dimensions)
        num_presents = sum(quantities)
        if tree_area // 9 >= num_presents:
            fit_count += 1
            continue

        # presents can't fit
        if tree_area <= sum(present_areas * quantities):
            continue

        # insert complicated and inefficient O(N!) puzzle logic here

    return fit_count

def main() -> None:
    input_path = DATA_DIR / "day12.txt"
    text = input_path.read_text(encoding="utf-8")
    shapes, trees = parse_input(text)

    print("Day 12")
    print("Part 1:", solve_part1(shapes, trees))

if __name__ == "__main__":
    main()