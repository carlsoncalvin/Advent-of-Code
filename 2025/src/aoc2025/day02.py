from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def parse_input(text: str) -> list[str]:
    return text.strip().split(",")

def is_double_sequence(number: int) -> bool:
    '''Check if a number is a double sequence for part 1'''
    str_number = str(number)
    # false if not even
    if len(str_number) % 2 != 0:
        return False
    # return first half == second half
    half = len(str_number) // 2
    return str_number[:half] == str_number[half:]

def is_repeated_sequence(number: int) -> bool:
    '''Check if a number is a repeated sequence for part 2. Now featuring sets and better names.'''
    str_number = str(number)
    max_block = len(str_number) // 2
    for block_size in range(max_block, 0, -1):
        if len(str_number) % block_size != 0:
            continue
        blocks = [str_number[i:i+block_size] for i in range(0, len(str_number), block_size)]
        if len(set(blocks)) == 1:
            return True
    return False

def solve_part1(ranges: list[str]) -> int:
    total = 0
    # brute-force loop over all numbers in range and check if doubled
    for num_range in ranges:
        start, end = map(int, num_range.split("-"))
        for number in range(start, end + 1):
            if is_double_sequence(number):
                total += number
    return total

def solve_part2(ranges: list[str]) -> int:
    total = 0
    # another brute force loop over all ranges
    for num_range in ranges:
        start, end = map(int, num_range.split("-"))
        for number in range(start, end + 1):
            if is_repeated_sequence(number):
                total += number
    return total

def main() -> None:
    input_path = DATA_DIR / "day02.txt"
    text = input_path.read_text(encoding="utf-8")
    ranges = parse_input(text)

    print("Day 2")
    print("Part 1:", solve_part1(ranges))
    print("Part 2:", solve_part2(ranges))

if __name__ == "__main__":
    main()
