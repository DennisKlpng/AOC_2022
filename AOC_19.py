import utils
import sys
import time
import math
from functools import lru_cache


@lru_cache(maxsize=10000)
def get_time_to_build(costs, e, c, o, robots, rob_ind):
    if rob_ind == 0:
        if e >= costs[0]:
            return 1
        return math.ceil((costs[0]-e)/robots[0] + 1)
    elif rob_ind == 1:
        if e >= costs[1]:
            return 1
        return math.ceil((costs[1]-e)/robots[0] + 1)
    elif rob_ind == 2:
        if e >= costs[2] and c >= costs[3]:
            return 1
        return math.ceil(max(1 + (costs[2]-e)/robots[0], 1 + (costs[3]-c)/robots[1])) if robots[1] > 0 else math.inf
    else:
        if e >= costs[4] and o >= costs[5]:
            return 1
        return math.ceil(max(1 + (costs[4]-e)/robots[0], 1 + (costs[5]-o)/robots[2])) if robots[2] > 0 else math.inf


def get_geodes_for_bp(bp, total_time):
    bp = tuple(bp)
    stack = [(total_time, 0, 0, 0, (1, 0, 0, 0), 0)]  # rem. time, num e, num c, num o, tuple of robots (e, c, o, g), geodes
    curr_max_g = 0
    while stack:
        # if start_print:
        #     print(stack)
        rt, e, c, o, robots, g = stack.pop()
        if rt <= 1:
            curr_max_g = max(curr_max_g, g)
            continue
        if g + (pow(rt-1, 2) + rt - 1)/2 < curr_max_g:
            continue
        # we have 4 possible states: wait until one of each kind of robot is buildable, then build it
        # pointless to build more ore robots than can be used in one step. Otherwise, build one
        if not robots[0] >= max(bp[0], bp[1], bp[2], bp[4]):
            nt = get_time_to_build(bp, e, c, o, robots, 0)
            stack.append((rt - nt, e-bp[0]+nt*robots[0], c+robots[1]*nt, o+robots[2]*nt, (robots[0]+1, robots[1], robots[2], robots[3],), g))
        # pointless to build more clay robots than can be used in one step. Otherwise, build one
        if not robots[1] >= bp[3]:
            nt = get_time_to_build(bp, e, c, o, robots, 1)
            stack.append((rt - nt, e-bp[1]+nt*robots[0], c+robots[1]*nt, o+robots[2]*nt, (robots[0], robots[1] + 1, robots[2], robots[3],), g))
        # pointless to build more obsidian robots than can be used in one step. Otherwise, build one
        if not robots[2] >= bp[5]:
            nt = get_time_to_build(bp, e, c, o, robots, 2)
            if nt != math.inf:
                stack.append((rt-nt, e-bp[2]+nt*robots[0], c-bp[3]+nt*robots[1], o+nt*robots[2], (robots[0], robots[1],
                                                                                                  robots[2] + 1, robots[3],), g))
        nt = get_time_to_build(bp, e, c, o, robots, 3)
        if nt != math.inf and rt > nt:
            stack.append((rt-nt, e-bp[4]+nt*robots[0], c+nt*robots[1], o-bp[5]+nt*robots[2], (robots[0], robots[1], robots[2], robots[3] + 1,), g + rt - nt))

    return curr_max_g


# abbreviations: e = ore, c = clay, o = obsidian, g = geode
if __name__ == '__main__':
    start_time = time.time()
    if sys.argv[1].startswith("Test"):
        bps = [''.join(x) for x in utils.split_fileinput_by_emptylines(sys.argv[1])]
    else:
        bps = utils.read_file_as_lines(sys.argv[1])
    bps = [utils.extract_int_list_from_string(x) for x in bps]

    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    # format: [0]: index, [1]: e cost e, [2]: c cost e, [3], [4] o cost e, c, [5], [6] g cost e, o
    quality = 0
    for x in bps:
        g_new = get_geodes_for_bp(x[1:], 24)
        quality += g_new * x[0]
    stop_time = time.time()
    assert quality == 33 if sys.argv[1].startswith("Test") else 1349
    print(f"pt1 solution: {quality} time overall: {stop_time - start_time}")
    start_time = stop_time
    score = 1
    for x in bps[0:3]:
        g_new = get_geodes_for_bp(x[1:], 32)
        print(f"geode {x[0]}, score: {g_new}")
        score *= g_new
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
