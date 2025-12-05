from pathlib import Path

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> list[str]:
    return text.strip().splitlines()

def get_ranges(lines: list[str]) -> tuple[list[tuple[int, int]], int]:
    '''
    Gets the ranges and the index of the first value line. The ranges are tuples of (start, end).
    '''
    ranges = []
    for i, line in enumerate(lines):
        if "-" not in line:
            break
        start, end = map(int, line.split("-"))
        if start > end:
            start, end = end, start
        ranges.append((start, end))
    values_start = i + 1

    return ranges, values_start

def get_values(lines: list[str], values_start) -> list[int]:
    """Converts all the values to integers and returns them as a new list."""
    values = []
    for line in lines[values_start:]:
        values.append(int(line))
    return values

def solve_part1(lines: list[str]) -> int:
    """Counts all the spoiled food and returns the number of unspoiled foods."""
    ranges, values_start = get_ranges(lines)
    values = get_values(lines, values_start)
    count = 0
    for value in values:
        spoiled = True
        for start, end in ranges:
            if start <= value <= end:
                spoiled = False
                break
        if spoiled:
            count += 1
    return len(values) - count

# Part 2
# I know I could just define a set and run through every range adding every value to that set,
# but I want to solve this without brute force. Maybe even elegantly (wishful thinking)

def solve_part2(lines: list[str]) -> int:
    """
    Sorts the ranges and then iterates through them, sequentially adding them to a new list.
    If two ranges overlap, they are combined, and the smaller range is removed from the new list
    and the new, expanded range is added. This continues until all ranges have been added.
    """
    # sort will sort according to first element, then the next. this should allow me to squash
    # everything together in one go
    ranges, _ = get_ranges(lines)
    ranges.sort()
    new_ranges = [ranges[0]]

    start, end = ranges[0]
    start2, end2 = ranges[1]
    iter = 2    # iterates through the original ranges
    ticker = 0  # tracks the new ranges. goes up when no more overlap

    # this could be a while True, but that seems sloppy
    # The while loop squashes the ranges down into each other
    while iter < len(ranges) + 1 and ticker < len(new_ranges) + 1:
        if start <= start2 <= end:
            new_ranges.pop(ticker)
            new_ranges.append((min(start, start2), max(end, end2)))
            start, end = new_ranges[ticker]
            if iter == len(ranges):
                break
            start2, end2 = ranges[iter]
            iter += 1
        else:
            new_ranges.append((start2, end2))
            start, end = start2, end2
            start2, end2 = ranges[iter]
            ticker += 1
            iter += 1

    # now just have to count the values
    count = 0
    for start, end in new_ranges:
        count += end - start + 1
    return count

def main() -> None:
    input_path = DATA_DIR / "day05.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 5")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()
