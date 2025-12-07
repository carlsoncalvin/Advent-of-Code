from pathlib import Path

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> list[str]:
    return text.splitlines()

def solve_part1(lines: list[str]) -> int:
    beam = {lines[0].index("S")} # set that tracks beam locations
    count = 0
    for line in lines:
        splitters = [i for i, e in enumerate(line) if e == "^"] # find splitters
        old_beam = beam.copy()
        for b in old_beam:
            if b in splitters:
                count += 1
                beam.remove(b)
                beam.update([b-1, b+1])
    return count

def solve_part2(lines: list[str]) -> int:
    tachyons = [0]*len(lines[0]) # now we track tachyons instead of beam locations
    tachyons[lines[0].index("S")] = 1
    for line in lines:
        splitters = [i for i, e in enumerate(line) if e == "^"]
        for s in splitters:
            if tachyons[s] != 0:
                tachyons[s-1] += tachyons[s]
                tachyons[s+1] += tachyons[s]
                tachyons[s] = 0
    return sum(tachyons)

def main() -> None:
    input_path = DATA_DIR / "day07.txt"
    text = input_path.read_text(encoding="utf-8")
    lines = parse_input(text)

    print("Day 7")
    print("Part 1:", solve_part1(lines))
    print("Part 2:", solve_part2(lines))

if __name__ == "__main__":
    main()