from pathlib import Path
import itertools
import numpy as np
from numpy import ndarray, dtype
from scipy.optimize import linprog

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> list[list[str]]:
    lines = [line.split() for line in text.strip().splitlines()]
    return lines

def parse_buttons(line: list[str]) -> tuple[ndarray[tuple[int, int], dtype[int]],
                                      ndarray[tuple[int, ...], dtype[int]]]:
    """Parses out the button and target information for part 1"""
    target = np.array([0 if b == "." else 1 for b in line[0].strip("[]")])
    raw_buttons = line[1:-1]
    buttons = np.zeros((len(target), len(raw_buttons)), dtype=int)
    for i, button in enumerate(raw_buttons):
        button = button.strip("()").split(",")
        for idx in button:
            buttons[int(idx), i] = 1
    return buttons, target

def press_buttons(buttons, target) -> int | Exception:
    """finds the minimum sum of button presses to reach the target lights."""
    # get all possible combinations of 0's and 1's - you´ll never have to press a button twice
    combos = np.array(list(itertools.product([0, 1], repeat=buttons.shape[1])))
    # sort by number of presses (sum)
    combos = sorted(combos, key=lambda x: np.sum(x))
    for combo in combos:
        # mod aritmetic keeps things binary
        if np.array_equal(np.sum(buttons * combo, axis=1)  % 2, target):
            return np.sum(combo)
    return Exception("No solution found")

def solve_part1(lines: list[list[str]]) -> int:
    count = 0
    for line in lines:
        # parse
        buttons, target = parse_buttons(line)
        # press
        count += press_buttons(buttons, target)
    return count

# part 2
def parse_joltage(line: list[str]) -> tuple[ndarray[tuple[int, int], dtype[int]],
                                      ndarray[tuple[int, ...], dtype[int]]]:
    """Parses out the button and target information for part 2"""
    target = np.array([int(j) for j in line[-1].strip("{}]").split(",")])
    raw_buttons = line[1:-1]
    buttons = np.zeros((len(target), len(raw_buttons)), dtype=int)
    for i, button in enumerate(raw_buttons):
        button = button.strip("()").split(",")
        for idx in button:
            buttons[int(idx), i] = 1
    return buttons, target

def press_more_buttons(buttons, target) -> int:
    """
    I tried: scipy lsq_linear, scipy nnls, scipy milp, numpy.linalg.lstsq, and numpy.linalg.solve
    before finding linprog. They all work on the test data, but fail on the puzzle data. It's was
    bit of a pain to understand the input, and I started timing out the AoC answer input, but once
    discovering the integrality contraint I made it work (also in under a second).
    I really didn't want to brute force it, but maybe I should have tried to see how long it would
    take.
    """
    c = np.ones(buttons.shape[1])
    res = linprog(c, A_eq=buttons, b_eq=target, bounds=(0, np.inf), integrality=1)
    return int(sum(res.x))

def solve_part2(lines: list[list[str]]) -> int:
    count = 0
    for line in lines:
        buttons, target = parse_joltage(line)
        count += press_more_buttons(buttons, target)
    return count

def main() -> None:
    input_path = DATA_DIR / "day10.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 10")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()