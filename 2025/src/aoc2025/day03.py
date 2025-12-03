from pathlib import Path

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
WINDOW = 12

# parser
def parse_input(text: str) -> list[str]:
    return text.strip().splitlines()

# part 1
def solve_part1(lines: list[str]) -> int:
    joltage = 0
    for line in lines:
        first_max_digit = max(line[:-1])
        idx = line.index(first_max_digit)
        second_max_digit = max(line[idx + 1:])
        joltage += int(first_max_digit + second_max_digit)
    return joltage

# part 2
def find_max_subsequence(line: str) -> int:
    '''
    Given a line of digits, find the maximum-valued 12-digit sequence without rearranging the
    digits. Uses a monotonic stack algorithm that drops small valued elements, rather than the
    "find the largest" approach I used before. Should be faster.
    '''
    n = len(line)

    drops_allowed = n - WINDOW
    stack = []

    for digit in line:
        # walk down the number and append values to stack, then pop the smallest while: 1, we still
        # can drop values and 2, the last value is smaller than the current value
        while drops_allowed > 0 and stack and stack[-1] < digit:
            stack.pop()
            drops_allowed -= 1
        stack.append(digit)

    result = "".join(stack[:WINDOW])

    return int(result)

def solve_part2(lines: list[str]) -> int:
    return sum(map(find_max_subsequence, lines))

def main() -> None:
    input_path = DATA_DIR / "day03.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 2")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()
