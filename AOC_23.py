import utils
import sys
import time
from collections import defaultdict
import numpy as np
import itertools


def vis(dct):
    l_vals, c_vals = [x[0] for x in dct.keys()], [x[1] for x in dct.keys()]
    l_min, l_max, c_min, c_max = int(min(l_vals)), int(max(l_vals)), int(min(c_vals)), int(max(c_vals))
    np_array_dct = np.zeros((l_max - l_min + 1, c_max - c_min + 1,))
    for key, val in dct.items():
        np_array_dct[(key[0] - l_min, key[1] - c_min,)] = val
    for l in range(l_max - l_min + 1):
        for c in range(c_max - c_min + 1):
            if np_array_dct[(l, c,)] == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


if __name__ == '__main__':
    start_time = time.time()
    elves_map = np.array([[1 if x is "#" else 0 for x in line] for line in utils.read_file_as_lines(sys.argv[1])])
    diml, dimc = np.shape(elves_map)
    elves_map_new = defaultdict(int)
    for l, c in itertools.product(range(diml), range(dimc)):
        elves_map_new[(l, c, )] = elves_map[(l, c)]
    elves_map = elves_map_new

    # vis(elves_map)
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    dir_check = (((-1, -1,), (-1, 0,), (-1, 1,)),  # north
                 ((1, -1,), (1, 0,), (1, 1,)),  # south
                 ((-1, -1,), (0, -1,), (1, -1,)),  # left
                 ((-1, 1,), (0, 1,), (1, 1,))  # right
                 )
    counter = 0

    def do_step(dir_check, steps):
        do_move = False
        # propose steps
        proposed_steps = {}
        elves = set([key for key, val in elves_map.items() if val == 1])
        for e in elves:
            e = tuple(e)
            nb = [(x[0], x[1]) for x in utils.get_diagneighbours(e)]
            if all([elves_map[x] == 0 for x in nb]):
                continue
            for d in range(4):
                d = (d + counter) % 4
                means = [sum([x[0] for x in dir_check[d]])/3, sum([x[1] for x in dir_check[d]])/3]
                if all([elves_map[x[0] + e[0], x[1] + e[1]] == 0 for x in dir_check[d]]):
                    proposed_steps.setdefault((int(e[0] + means[0]), int(e[1] + means[1])), []).append(e)
                    break
        # check if proposed steps are unique
        for newpos, oldpos in proposed_steps.items():
            if len(oldpos) == 1:
                do_move = True
                elves_map[oldpos[0]] = 0
                elves_map[newpos] = 1

        return steps + 1, do_move

    for i in range(10):
        counter, did_move = do_step(dir_check, counter)

    def calc_score():
        # done, calculate final result
        l_vals, c_vals = [x[0] for x, y in elves_map.items() if y == 1], [x[1] for x, y in elves_map.items() if y == 1]
        l_min, l_max, c_min, c_max = int(min(l_vals)), int(max(l_vals)), int(min(c_vals)), int(max(c_vals))
        return (l_max - l_min + 1) * (c_max - c_min + 1) - len(l_vals)

    score = calc_score()
    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == 110
    print(f"pt1 solution: {score.real} time overall: {stop_time - start_time}")
    while True:
        counter, did_move = do_step(dir_check, counter)
        if not did_move:
            break
    score = counter
    if sys.argv[1].startswith("Test"):
        assert score == 20
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
