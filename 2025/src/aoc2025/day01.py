from pathlib import Path
import math

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DIAL_LENGTH = 100
DIRECTION = {"R": 1, "L": -1}

# parser
def parse_input(text: str) -> list[str]:
    return text.strip().splitlines()

# part 1
def solve_part1(lines: list[str]) -> int:
    position = 50
    zero_count = 0

    for line in lines:
        direction_change = DIRECTION[line[0]]
        steps = int(line[1:])
        delta = direction_change * steps

        position = (position + delta) % DIAL_LENGTH

        if position == 0:
            zero_count += 1

    return zero_count

# part 2
def solve_part2(lines: list[str]) -> int:
    '''
    A nice implementation that uses intervals to avoid counting crossings with modulo arithmetic
    and conditionals for each eventuality. Also uses an unbounded range rather than resetting to a
    "real" position at the end of each move.
    '''
    position = 50
    crossings = 0

    for line in lines:
        direction_change = DIRECTION[line[0]]
        steps = int(line[1:])

        # define an ordered interval [a, b] for the move describing positions visited
        # EXCLUDING the starting point
        if direction_change == 1:
            a = position + 1
            b = position + steps
        else:
            a = position - steps
            b = position - 1

        # count how many crossings in [a, b]
        # ceiling for min and floor for max
        # if not a multiple of 100 in the range then the conditional fails
        k_min = math.ceil(a / DIAL_LENGTH)
        k_max = math.floor(b / DIAL_LENGTH)
        if k_max >= k_min:
            crossings += k_max - k_min + 1

        position += direction_change * steps

    return crossings

def main() -> None:
    input_path = DATA_DIR / "day01.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 1")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()
