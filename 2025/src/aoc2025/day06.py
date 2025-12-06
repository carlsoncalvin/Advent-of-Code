from pathlib import Path
import numpy as np

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
OP_DICT = {"*": np.prod, "+": np.sum}

# parser
def parse_input(text: str) -> list[str]:
    return text.splitlines()

def solve_part1(lines: list[str]) -> int:
    """Sends each column of numbers to the appropriate operation and sums the results."""
    lines = lines.copy() # make a copy of lines so part 2 doesn't get messed up
    operations = lines.pop(-1).split() # get row of operations
    numbers = np.array([line.strip().split() for line in lines], dtype=int) # get integers
    total = 0
    for col in range(numbers.shape[1]):
        # perform operation on each column of numbers
        total += OP_DICT[operations[col]](numbers[:, col])
    return total

def solve_part2(lines: list[str]) -> int:
    """
    Identifies the start of each column of numbers and stacks them vertically. Then, for each stack,
    uses list comprehension to combine the nth digit of each line and performs the appropriate
    operation on the resulting strings (converted to int). The final result is summed.
    """
    operations = lines.pop(-1)
    # identify the start of each column
    col_starts = [idx for idx in range(len(operations)) if operations[idx] != " "]
    total = 0
    for i, col in enumerate(col_starts):
        end = col_starts[i+1] if i+1 < len(col_starts) else len(operations) # find end of column
        line_stack = [line[col:end] for line in lines] # get lines of only this problem

        # get numbers from right to left, joined vertically
        numbers = ["".join([line[-n].strip() for line in line_stack])
                   for n in range(1, len(line_stack[0]) + 1)]

        # if len(num) accounts for empty string caused by the whitespace column between problems
        total += OP_DICT[operations[col]]([int(num) for num in numbers if len(num)])

    return total
# I realized that I don't have to go from right to left when joining the stacks, but I
# think I'll just leave the code how it is. It's a bit more convoluted than it needs to be, but
# i'll keep it for posterity

def main() -> None:
    input_path = DATA_DIR / "day06.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 6")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()