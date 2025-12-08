from pathlib import Path
from typing import Any

import numpy as np
from numpy import ndarray, dtype
from scipy.spatial.distance import pdist

# constants
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# parser
def parse_input(text: str) -> ndarray[tuple[int, ...], dtype[float]]:
    lines = text.strip().splitlines()
    lines = [line.split(",") for line in lines]
    return np.array(lines, dtype=float)

# I really hate this solution. I really struggled with figuring out how to track the circuits.
# The method I landed on was to use a list of sets and add box indices to the sets in order of
# shortest connections, but this requires some awful logic to account for joining circuits.
# I did not have a nice time with this puzzle, so I probably won't return to it and make it better
def solve_puzzle(coords: ndarray[tuple[int, ...], dtype[float]],
                 n_connections=1000,
                 part2=False) -> int:
    # use scipy to compute all pairwise distances quickly
    dist_array = pdist(coords)
    m = len(coords)

    if part2:
        master_set = set(range(m))
        n_connections = len(dist_array) + 1

    # get indicies of pairs ordered as pdist output
    pair_idxs = np.array([(i, j) for i in range(m) for j in range(i+1, m)], dtype=int)

    # sort by shortest distances
    sorted_idxs = np.argsort(dist_array)

    # only care about boxes, not the distances themselves
    sorted_pair_idxs = pair_idxs[sorted_idxs]

    # find which circuits should be created
    circuits = []
    for i, j in sorted_pair_idxs[:n_connections]:
        in_circuit = [None, None]
        for idx, circuit in enumerate(circuits):
            if i in circuit:
                in_circuit[0] = idx
            if j in circuit:
                in_circuit[1] = idx

        if all(in_circuit):
            i_c, j_c = in_circuit
            # both in different circuits: join
            if i_c != j_c:
                circuits[i_c].update(circuits[j_c])
                circuits.remove(circuits[j_c])
                n_connections -= 1
            # both in same circuit: do nothing
            else:
                n_connections -= 1
        # only 1 in circuit
        elif any(in_circuit) and not all(in_circuit):
            idx = [idx for idx in in_circuit if idx is not None][0]
            circuits[idx].update([i, j])
            n_connections -= 1
        # none in circuit
        elif not any(in_circuit):
            circuits.append({i, j})
            n_connections -= 1
        else:
            raise ValueError("Something went wrong")
        if part2:
            for circuit in circuits:
                if circuit == master_set:
                    return int(coords[i][0] * coords[j][0])

    circuits.sort(key=len, reverse=True)
    return int(np.prod([len(circuits[i]) for i in range(len(circuits)) if i < 3]))

def main() -> None:
    input_path = DATA_DIR / "day08.txt"
    text = input_path.read_text(encoding="utf-8")
    coords = parse_input(text)

    print("Day 8")
    print("Part 1:", solve_puzzle(coords))
    print("Part 2:", solve_puzzle(coords, part2=True))

if __name__ == "__main__":
    main()