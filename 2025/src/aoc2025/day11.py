from pathlib import Path
import datetime

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> dict[str, str]:
    lines = text.strip().splitlines()
    device_dict = {}
    for line in lines:
        device, connections = line.split(":")
        device_dict[device] = connections.split()
    return device_dict

def dfs(start: str, end: str, device_dict: dict[str, str], visited=None,
        all_paths=None, part2 = False, seen_dac=False) -> list[list[str]] | None:
    if visited is None:
        visited = [start]
    if all_paths is None:
        all_paths = []
    if start == end:
        if part2 and "fft" in visited:
            print("found path")
            all_paths.append(list(visited))
        elif not part2:
            all_paths.append(list(visited))
        return None

    for node in device_dict[start]:
        # dac comes first in my set
        if part2 and node == "dac":
            seen_dac = True
        # if we encounter fft before dac we break
        if part2 and node == "fft" and not seen_dac:
            return None
        if node not in visited:
            visited.append(node)
            dfs(node, end,  device_dict, visited, all_paths, part2=part2, seen_dac=seen_dac)
            visited.pop()

    return all_paths

def solve_part1(device_dict: dict[str, str]) -> int:
    all_paths = dfs("you", "out", device_dict)
    return len(all_paths)

def solve_part2(device_dict: dict[str, str]) -> int:
    start_time = datetime.datetime.now()
    print(start_time.time(), "part 2 started")

    all_paths = dfs("svr", "out", device_dict, part2=True)

    end_time = datetime.datetime.now()
    print(end_time.time(), "part 2 ended")
    total_time = end_time - start_time
    print(total_time, "total time")

    return len(all_paths)

def main() -> None:
    input_path = DATA_DIR / "day11.txt"
    text = input_path.read_text(encoding="utf-8")
    device_dict = parse_input(text)

    print("Day 11")
    print("Part 1:", solve_part1(device_dict))
    print("Part 2:", solve_part2(device_dict))

if __name__ == "__main__":
    main()
