import utils
import sys
import time
from collections import Counter
import numpy as np


if __name__ == '__main__':
    start_time = time.time()
    elves_map = np.array([[1 if x is "#" else 0 for x in line] for line in utils.read_file_as_lines(sys.argv[1])])
    print(elves_map)
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    dimx, dimy = np.shape(elves_map)
    dir_check = np.array([[[-1, -1], [-1, 0], [-1, 1]],  # north
                 [[1, -1], [1, 0], [1, 1]],  # south
                 [[-1, -1], [0, -1], [1, -1]],
                 [[-1, 1], [0, 1], [1, 1]],
                 ])
    # print(dir_check)
    for i in range(10):
        # propose steps
        proposed_steps = {}
        elves = np.argwhere(elves_map == 1)
        # print(dir_check[0])
        # print(np.mean(dir_check[0], axis=0))
        for e in elves:
            e = tuple(e)
            # print(e)
            nb = [(x[0], x[1]) for x in utils.get_diagneighbours(e) if 0 <= x[0] < dimx and 0 <= x[1] < dimy]
            if all([elves_map[x] == 0 for x in nb]):
                # print(f"Continuing for elf at pos {e}")
                continue
            # print(f"Analyzing e: {e}")
            for d in range(3):
                # print(f"e: {e} d: {d}")
                means = np.mean(dir_check[d], axis=0)
                if all([elves_map[x[0] + e[0], x[1] + e[1]] == 0 for x in dir_check[d]]):
                    proposed_steps[e] = (int(e[0] + means[0]), int(e[1] + means[1]))
                    break
                # tgt = False
                # for x in dir_check[d]:
                #     print(f"for d: {d}, x: {x}, map: {elves_map[x[0] + e[0], x[1] + e[1]]}")
                #     if elves_map[x[0] + e[0], x[1] + e[1]] != 0:
                #         tgt = True
                #         print("Tgt in range")
                # print(f"tgt pos: {e[0] + means[0]}, {e[1] + means[1]}")
                # if 0 < e[0] + means[0] < (dimx - 1) and 0 < e[1] + means[1] < (dimy - 1) and not tgt:
                #     proposed_steps[e] = (int(e[0] + means[0]), int(e[1] + means[1]))
                #     break

        # print(proposed_steps)
        # check if proposed steps are unique
        seen = set()
        dupes = [x for x in proposed_steps.values() if x in seen or seen.add(x)]
        for oldpos, newpos in proposed_steps.items():
            if newpos not in dupes:
                elves_map[oldpos] = 0
                elves_map[newpos] = 1

        print(elves_map)
        dir_check = np.roll(dir_check, -1, axis=0)
        # print(dir_check)

        # score = move_maze(curr_pos, instructions)
    # stop_time = time.time()
    # if Test:
    #     assert score == 6032
    # print(f"pt1 solution: {score.real} time overall: {stop_time - start_time}")
    # score = move_maze(curr_pos, instructions, True)
    # if Test:
    #     assert score == 5031
    # stop_time = time.time()
    # print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
