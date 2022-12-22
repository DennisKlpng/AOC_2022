import utils
import sys
import time
import re
import math


def move_maze(in_pos, in_instr, pt2=False):
    in_dir = (1, 0,)
    for inst in in_instr:
        if inst.isnumeric():
            in_pos = modify_pos(in_pos, in_dir, int(inst))
            continue
        elif inst == "R":
            # rotate clockwise
            in_dir = rotate_clock(in_dir)
        else:
            # rotate counterclockwise
            in_dir = rotate_ctclock(in_dir)
        # print(f"New pos: {curr_pos}, new direction: {direction}")
    dir_assosc = {(1, 0, ): 0, (0, 1,): 1, (-1, 0,): 2, (0, -1,): 3}
    col, row, dir_val = in_pos[0] + 1, in_pos[1] + 1, dir_assosc[in_dir]
    return 1000*row + 4*col + dir_val


def modify_pos(position, dirct, step_length):
    new_pos = position
    available_pos = maze_pts.keys()
    for step in range(int(step_length)):
        tgt_pos = new_pos
        while True:
            tgt_pos = (tgt_pos[0] + dirct[0], tgt_pos[1] + dirct[1],)
            tgt_pos = list(tgt_pos)

            if tgt_pos[0] < 0:
                tgt_pos[0] = dim_x - 1
            elif tgt_pos[0] >= dim_x:
                tgt_pos[0] = 0
            if tgt_pos[1] < 0:
                tgt_pos[1] = dim_y - 1
            elif tgt_pos[1] >= dim_y:
                tgt_pos[1] = 0
            tgt_pos = tuple(tgt_pos)

            if tgt_pos in available_pos:
                if maze_pts[tgt_pos] == "#":
                    return new_pos
                new_pos = tgt_pos
                break
    return new_pos


if __name__ == '__main__':
    start_time = time.time()
    maze = utils.read_file_as_lines(sys.argv[1])
    instructions = maze[-1]
    instructions = [x for x in re.split('(\d+)', instructions.strip()) if x != ""]
    maze = maze[0:-2]
    dim_x, dim_y = max([len(x) for x in maze]), len(maze)
    maze_pts = dict()
    curr_pos = None
    for y in range(dim_y):
        for x in range(len(maze[y])):
            if maze[y][x] != " ":
                maze_pts[(x, y,)] = maze[y][x]
                if not curr_pos:
                    curr_pos = (x, y,)

    r_90, r_m90 = math.radians(90), math.radians(-90)
    mat_clock = (int(math.cos(r_90))), int(-math.sin(r_90)), int(math.sin(r_90)), int(math.cos(r_90))
    mat_ctclock = (int(math.cos(r_m90))), int(-math.sin(r_m90)), int(math.sin(r_m90)), int(math.cos(r_m90))

    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time

    def rotate_clock(dirct):
        return tuple((mat_clock[0]*dirct[0] + mat_clock[1]*dirct[1], mat_clock[2]*dirct[0] + mat_clock[3]*dirct[1]))

    def rotate_ctclock(dirct):
        return tuple((mat_ctclock[0]*dirct[0] + mat_ctclock[1]*dirct[1], mat_ctclock[2]*dirct[0] + mat_ctclock[3]*dirct[1]))

    score = move_maze(curr_pos, instructions)

    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == 6032
    print(f"pt1 solution: {score.real} time overall: {stop_time - start_time}")
    if sys.argv[1].startswith("Test"):
        assert score == 5031
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
