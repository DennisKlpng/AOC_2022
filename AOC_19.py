import utils
import sys
import time
from functools import lru_cache


@lru_cache(maxsize=10000)
def check_if_robot_buildable(costs, e, c, o):
    available_robots = []
    if e >= costs[0]:
        available_robots.append(0)
    if e >= costs[1]:
        available_robots.append(1)
    if e >= costs[2] and c >= costs[3]:
        available_robots.append(2)
    if e >= costs[4] and o >= costs[5]:
        available_robots.append(3)
    return tuple(available_robots)


def get_geodes_for_bp(bp):
    bp = tuple(bp)
    stack = [(24, 0, 0, 0, (1, 0, 0), 0)]  # rem. time, num e, num c, num o, tuple of robots (e, c, o, g), geodes
    curr_max_g = 0
    while stack:
        # print(stack)
        rt, e, c, o, robots, g = stack.pop()
        if rt == 1:  # building robots is pointless now
            curr_max_g = max(curr_max_g, g)
            continue
        # if g + (pow(rt-1, 2) + rt - 1)/2 < curr_max_g:
        #     continue
        rt -= 1
        info = check_if_robot_buildable(bp, e, c, o)
        e += robots[0]
        c += robots[1]
        o += robots[2]
        robots = list(robots)
        # since we just count the num of geodes, we don't need to track bots, just immediately add the geodes
        # they will produce to the state geode count
        if 3 in info:
            stack.append((rt, e - bp[4], c, o - bp[5], tuple(robots), g + rt))
            continue
        # pointless to build more ore robots than can be used in one step
        if 0 in info and not robots[0] >= max(bp[0], bp[1], bp[2], bp[4]):
            stack.append((rt, e - bp[0], c, o, (robots[0]+1, robots[1], robots[2],), g))
        # pointless to build more clay robots than can be used in one step
        if 1 in info and not robots[1] >= bp[3]:
            stack.append((rt, e - bp[1], c, o, (robots[0], robots[1]+1, robots[2],), g))
        # pointless to build more obsidian robots than can be used in one step
        if 2 in info and not robots[2] >= bp[4]:
            stack.append((rt, e - bp[2], c - bp[3], o, (robots[0], robots[1], robots[2]+1,), g))
        elif not len(info) == 4:  # if all robots buidable, it's a waste to not build one
            stack.append((rt, e, c, o, tuple(robots), g, ))

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
    max_g = 0
    for x in bps:
        g_new = get_geodes_for_bp(x[1:])
        max_g = max(max_g, g_new)
        print(f"geodes: {g_new} for bp: {x}")
    stop_time = time.time()
    print(f"pt1 solution: {max_g} time overall: {stop_time - start_time}")
    start_time = stop_time
    #
    # stop_time = time.time()
    # print(f"pt2 solution: {} time overall: {stop_time - start_time}")
