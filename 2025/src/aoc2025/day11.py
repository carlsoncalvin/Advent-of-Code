from pathlib import Path
import datetime
import functools

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> dict[str, list[str]]:
    lines = text.strip().splitlines()
    device_dict = {}
    for line in lines:
        device, connections = line.split(":")
        device_dict[device] = connections.split()
    return device_dict

def dfs(start: str, end: str, device_dict: dict[str, list[str]],
        visited=None, all_paths=None,) -> list[list[str]] | None:
    """
    My first deep first search algorithm. Runs fast on part 1. I tried modifying for part 2 but
    found a much better solution.
    """
    if visited is None:
        visited = [start]
    if all_paths is None:
        all_paths = []
    # exit recursion
    if start == end:
        all_paths.append(list(visited))
        return None

    for node in device_dict[start]:
        if node not in visited:
            visited.append(node)
            dfs(node, end,  device_dict, visited, all_paths)
            # pop path after end is reached
            visited.pop()

    return all_paths

def solve_part1(device_dict: dict[str, list[str]]) -> int:
    """Find all paths and return the length of the list."""
    all_paths = dfs("you", "out", device_dict)
    return len(all_paths)

# part 2:
# I couldn't figure out manual memoization but I found this caching decorator that works
@functools.lru_cache(maxsize=None)
def dfs_part2(node: str, target_tracker: tuple[int, int]) -> int:
    """
    The big realization here was that I don't need to actually track the paths traversed. I
    discovered that the graph is "directed acyclic" (thanks reddit) so I don't have to worry about
    getting caught in a loop. I can just track the number of times we hit the dac and fft nodes from
    any given path and cache the result. Then, at the end, sum the bool results.
    """
    # check if we passed targets once reaching end
    if node == "out":
        return target_tracker[0] + target_tracker[1] == 2

    # check if we hit dac or fft and update target tracker
    if node == "dac":
        target_tracker = (1, target_tracker[1])
    elif node == "fft":
        target_tracker = (target_tracker[0], 1)

    # do recursion
    total = 0
    for next_node in DEVICE_DICT[node]:
        total += dfs_part2(next_node, target_tracker)
    return total

def solve_part2() -> int:
    """
    Runs in less than 0.4 ms. Wasted a lot of time waiting for code to run before figuring out
    caching.
    """
    start_time = datetime.datetime.now()

    num_paths = dfs_part2("svr", (0, 0))

    end_time = datetime.datetime.now()
    print(end_time - start_time, "total time")

    return num_paths

def main() -> None:
    input_path = DATA_DIR / "day11.txt"
    text = input_path.read_text(encoding="utf-8")

    # have to make the input global so it doesn't need to be hashed in part 2
    global DEVICE_DICT
    DEVICE_DICT = parse_input(text)

    print("Day 11")
    print("Part 1:", solve_part1(DEVICE_DICT))
    print("Part 2:", solve_part2())

if __name__ == "__main__":
    main()
