import utils
import sys
import time
from collections import deque
from math import inf


def visualize_blizz(curr):
    curr = {x[0]: x[1] for x in curr}
    print(snow_map[0])
    for i in range(1, dim_h + 1):
        for j in range(dim_w + 2):
            if j == 0 or j == dim_w + 1:
                print("#", end="")
            elif (i, j) not in curr.keys():
                print(".", end="")
            elif curr[(i, j)] == (0, 1):
                print(">", end="")
            elif curr[(i, j)] == (0, -1):
                print("<", end="")
            elif curr[(i, j)] == (1, 0):
                print("v", end="")
            elif curr[(i, j)] == (-1, 0):
                print("^", end="")
        print()
    print(snow_map[-1])


if __name__ == '__main__':
    start_time = time.time()
    snow_map = utils.read_file_as_lines(sys.argv[1])
    start_pos, end_pos = (0, snow_map[0].index("."),), (len(snow_map) - 1, snow_map[-1].index("."))
    dim_w, dim_h = len(snow_map[0]) - 2, len(snow_map) - 2
    blizz_rpt = dim_w * dim_h

    blizz_inert = set()
    for l in range(1, len(snow_map) - 1):
        for c in range(1, len(snow_map[l]) - 1):
            if snow_map[l][c] == ">":
                blizz_inert.add(((l, c, ), (0, 1)))
            elif snow_map[l][c] == "<":
                blizz_inert.add(((l, c, ), (0, -1)))
            elif snow_map[l][c] == "v":
                blizz_inert.add(((l, c,), (1, 0)))
            elif snow_map[l][c] == "^":
                blizz_inert.add(((l, c,), (-1, 0)))


    def get_blizzards(step, debug=False):
        blizz_st_dbg = set()
        blizz_st = set()
        for b in blizz_inert:
            bl = (b[0][0] + step * b[1][0] - 1) % dim_h + 1
            bc = (b[0][1] + step * b[1][1] - 1) % dim_w + 1
            if debug:
                blizz_st_dbg.add(((bl, bc), (b[1][0], b[1][1]),))
            blizz_st.add((bl, bc))
        if debug:
            return blizz_st_dbg
        return blizz_st

    # precalc blizzard pos:
    blizz_pos = {i: get_blizzards(i) for i in range(max(1000, blizz_rpt))}

    # blizz_pos_dbg = {i: get_blizzards(i, True) for i in range(100)}
    # for i in blizz_pos_dbg.keys():
    #     visualize_blizz(blizz_pos_dbg[i])

    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time

    def bfs(start, tgt):
        stack = deque()
        stack.append(start)
        min_steps = inf
        visited = {start}
        while stack:
            pos, steps = stack.popleft()
            if pos == tgt:
                min_steps = min(min_steps, steps)
                break
            # get neighbors, append valid nb to stack
            nbs = utils.get_neighbours(pos)
            nbs.append(pos)
            for nb in nbs:
                if nb[0] > dim_h or nb[0] < 1 or nb[1] > dim_w or nb[1] < 1:
                    if nb != start[0] and nb != tgt:
                        continue
                # if nb != start_pos and (nb[0] > dim_h + 1 or nb[0] < 1 or nb[1] > dim_w + 1 or nb[1] < 1):  # outside
                if nb in blizz_pos[(steps + 1)]:
                    continue
                if (nb, (steps + 1) % blizz_rpt,) in visited:
                    continue
                elem = (nb, steps + 1,)
                visited.add((nb, (steps + 1) % blizz_rpt,))
                stack.append(elem)
        return min_steps

    score = bfs((start_pos, 0,), end_pos)
    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == 18
    print(f"pt1 solution: {score} time overall: {stop_time - start_time}")

    score = bfs((end_pos, score,), start_pos)
    score = bfs((start_pos, score,), end_pos)
    if sys.argv[1].startswith("Test"):
        assert score == 54
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
