import utils
import sys
import time
import re
import math

# Part1
test_move = {1: {'x+': (1, "minx", (1, 0,)), 'x-': (1, "maxx", (-1, 0,)), 'y+': (4, "miny", (0, 1,)), 'y-': (5, "maxy", (0, -1,))},
             2: {'x+': (3, "minx", (1, 0,)), 'x-': (4, "maxx", (-1, 0,)), 'y+': (2, "miny", (0, 1,)), 'y-': (2, "maxy", (0, -1,))},
             3: {'x+': (4, "minx", (1, 0,)), 'x-': (2, "maxx", (-1, 0,)), 'y+': (3, "miny", (0, 1,)), 'y-': (3, "maxy", (0, -1,))},
             4: {'x+': (2, "minx", (1, 0,)), 'x-': (3, "maxx", (-1, 0,)), 'y+': (5, "miny", (0, 1,)), 'y-': (1, "maxy", (0, -1,))},
             5: {'x+': (6, "minx", (1, 0,)), 'x-': (6, "maxx", (-1, 0,)), 'y+': (1, "miny", (0, 1,)), 'y-': (4, "maxy", (0, -1,))},
             6: {'x+': (5, "minx", (1, 0,)), 'x-': (5, "maxx", (-1, 0,)), 'y+': (6, "miny", (0, 1,)), 'y-': (6, "maxy", (0, -1,))},
             }

# TODO
real_move = {1: {'x+': (2, "minx", (1, 0,)), 'x-': (2, "maxx", (-1, 0,)), 'y+': (3, "miny", (0, 1,)), 'y-': (5, "maxy", (0, -1,))},
             2: {'x+': (1, "minx", (1, 0,)), 'x-': (1, "maxx", (-1, 0,)), 'y+': (2, "miny", (0, 1,)), 'y-': (2, "maxy", (0, -1,))},
             3: {'x+': (3, "minx", (1, 0,)), 'x-': (3, "maxx", (-1, 0,)), 'y+': (5, "miny", (0, 1,)), 'y-': (1, "maxy", (0, -1,))},
             4: {'x+': (5, "minx", (1, 0,)), 'x-': (5, "maxx", (-1, 0,)), 'y+': (6, "miny", (0, 1,)), 'y-': (6, "maxy", (0, -1,))},
             5: {'x+': (4, "minx", (1, 0,)), 'x-': (4, "maxx", (-1, 0,)), 'y+': (1, "miny", (0, 1,)), 'y-': (3, "maxy", (0, -1,))},
             6: {'x+': (6, "minx", (1, 0,)), 'x-': (6, "maxx", (-1, 0,)), 'y+': (4, "miny", (0, 1,)), 'y-': (4, "maxy", (0, -1,))},
             }
# Part2
# TODO
test_cube = {1: {'x+': (6, "maxx", (-1, 0,)), 'x-': (3, "miny", (0, 1,)), 'y+': (4, "miny", (0, 1,)), 'y-': (2, "miny", (0, 1,))},
             2: {'x+': (3, "minx", (1, 0,)), 'x-': (6, "maxy", (0, -1,)), 'y+': (5, "maxy", (0, -1,)), 'y-': (1, "miny", (0, -1,))},
             3: {'x+': (4, "minx", (1, 0,)), 'x-': (2, "maxx", (-1, 0,)), 'y+': (5, "minx", (1, 0,)), 'y-': (1, "minx", (1, 0,))},
             4: {'x+': (6, "miny", (0, 1,)), 'x-': (3, "maxx", (-1, 0,)), 'y+': (5, "miny", (0, 1,)), 'y-': (1, "maxy", (0, -1,))},
             5: {'x+': (6, "minx", (1, 0,)), 'x-': (3, "maxy", (0, -1,)), 'y+': (2, "maxy", (0, -1,)), 'y-': (4, "maxy", (0, -1,))},
             6: {'x+': (1, "maxx", (-1, 0,)), 'x-': (5, "maxx", (-1, 0,)), 'y+': (2, "minx", (1, 0,)), 'y-': (4, "maxx", (-1, 0,))},
             }

# TODO
real_cube = {1: {'x+': (2, "minx", (1, 0,)), 'x-': (4, "minx", (1, 0,)), 'y+': (3, "miny", (0, 1,)), 'y-': (6, "minx", (1, 0,))},
             2: {'x+': (5, "maxx", (-1, 0,)), 'x-': (1, "maxx", (-1, 0,)), 'y+': (3, "maxx", (-1, 0,)), 'y-': (6, "maxy", (0, -1,))},
             3: {'x+': (2, "maxy", (0, -1,)), 'x-': (4, "miny", (0, 1,)), 'y+': (5, "miny", (0, 1,)), 'y-': (1, "maxy", (0, -1,))},
             4: {'x+': (5, "minx", (1, 0,)), 'x-': (1, "minx", (1, 0,)), 'y+': (6, "miny", (0, 1,)), 'y-': (3, "minx", (1, 0,))},
             5: {'x+': (2, "maxx", (-1, 0,)), 'x-': (4, "maxx", (-1, 0,)), 'y+': (6, "maxx", (-1, 0,)), 'y-': (3, "maxy", (0, -1,))},
             6: {'x+': (5, "maxy", (0, -1,)), 'x-': (1, "miny", (0, 1,)), 'y+': (2, "miny", (0, 1,)), 'y-': (4, "maxy", (0, -1,))},
             }


def move_maze(in_pos, in_instr, pt2=False):
    in_dir = (1, 0,)
    for inst in in_instr:
        if inst.isnumeric():
            in_pos, in_dir = modify_pos(in_pos, in_dir, int(inst), pt2)
            continue
        elif inst == "R":  # rotate clockwise
            in_dir = rotate_clock(in_dir)
        else:  # rotate counterclockwise
            in_dir = rotate_ctclock(in_dir)
    dir_assosc = {(1, 0, ): 0, (0, 1,): 1, (-1, 0,): 2, (0, -1,): 3}
    col, row, dir_val = in_pos[0] + 1, in_pos[1] + 1, dir_assosc[in_dir]
    return 1000*row + 4*col + dir_val


def wrap_around(wrapper, orig_pos, tgt_face, orig_wrap):  # everyting hardcoded, see 3d built cube
    tgt_pos = list(orig_pos)
    t_lim = face_limits[tgt_face]
    o_lim = face_limits[orig_pos[2]]
    if orig_wrap == "x+":  # r =>
        if wrapper[1] == "minx":
            tgt_pos[0] = t_lim["min_x"]
            tgt_pos[1] = orig_pos[1] - o_lim["min_y"] + t_lim["min_y"]
        elif wrapper[1] == "maxx":
            tgt_pos[0] = t_lim["max_x"]
            tgt_pos[1] = t_lim["max_y"] - (orig_pos[1] - o_lim["min_y"])
        if wrapper[1] == "miny":
            tgt_pos[1] = t_lim["min_y"]
            tgt_pos[0] = t_lim["max_x"] - (orig_pos[1] - o_lim["min_y"])
        elif wrapper[1] == "maxy":
            tgt_pos[1] = t_lim["max_y"]
            tgt_pos[0] = orig_pos[1] - o_lim["min_y"] + t_lim["min_x"]
    elif orig_wrap == "x-":  # l =>
        if wrapper[1] == "minx":
            tgt_pos[0] = t_lim["min_x"]
            tgt_pos[1] = t_lim["max_y"] - (orig_pos[1] - o_lim["min_y"])
        elif wrapper[1] == "maxx":
            tgt_pos[0] = t_lim["max_x"]
            tgt_pos[1] = orig_pos[1] - o_lim["min_y"] + t_lim["min_y"]
        if wrapper[1] == "miny":
            tgt_pos[1] = t_lim["min_y"]
            tgt_pos[0] = orig_pos[1] - o_lim["min_y"] + t_lim["min_x"]
        elif wrapper[1] == "maxy":
            tgt_pos[1] = t_lim["max_y"]
            tgt_pos[0] = t_lim["max_x"] - (orig_pos[1] - o_lim["min_y"])
    elif orig_wrap == "y+":  # d =>
        if wrapper[1] == "minx":
            tgt_pos[0] = t_lim["min_x"]
            tgt_pos[1] = t_lim["max_y"] - (orig_pos[0] - o_lim["min_x"])
        elif wrapper[1] == "maxx":
            tgt_pos[0] = t_lim["max_x"]
            tgt_pos[1] = t_lim["min_y"] + orig_pos[0] - o_lim["min_x"]
        if wrapper[1] == "miny":
            tgt_pos[1] = t_lim["min_y"]
            tgt_pos[0] = orig_pos[0] - o_lim["min_x"] + t_lim["min_x"]
        elif wrapper[1] == "maxy":
            tgt_pos[1] = t_lim["max_y"]
            tgt_pos[0] = t_lim["max_x"] - (orig_pos[0] - o_lim["min_x"])
    elif orig_wrap == "y-":  # u =>
        if wrapper[1] == "minx":
            tgt_pos[0] = t_lim["min_x"]
            tgt_pos[1] = orig_pos[0] - o_lim["min_x"] + t_lim["min_y"]
        elif wrapper[1] == "maxx":
            tgt_pos[0] = t_lim["max_x"]
            tgt_pos[1] = t_lim["max_y"] - (orig_pos[0] - o_lim["min_x"])
        if wrapper[1] == "miny":
            tgt_pos[1] = t_lim["min_y"]
            tgt_pos[0] = t_lim["max_x"] - (orig_pos[0] - o_lim["min_x"])
        elif wrapper[1] == "maxy":
            tgt_pos[1] = t_lim["max_y"]
            tgt_pos[0] = orig_pos[0] - o_lim["min_x"] + t_lim["min_x"]

    tgt_pos[2] = tgt_face
    return tuple(tgt_pos)


def modify_pos(position, dirct, step_length, pt2):
    new_pos = position
    tgt_pos = position
    new_direction = dirct
    if not pt2:
        wrap = test_move if Test else real_move
    else:
        wrap = test_cube if Test else real_cube
    for step in range(int(step_length)):
        tgt_pos = (tgt_pos[0] + dirct[0], tgt_pos[1] + dirct[1], tgt_pos[2],)
        # wrap around
        if tgt_pos[0] > face_limits[tgt_pos[2]]["max_x"]:
            wrap_new = wrap[position[2]]['x+']
            dirct = wrap_new[2]
            tgt_pos = wrap_around(wrap_new, tgt_pos, wrap_new[0], 'x+')
        elif tgt_pos[0] < face_limits[tgt_pos[2]]["min_x"]:
            wrap_new = wrap[position[2]]['x-']
            dirct = wrap_new[2]
            tgt_pos = wrap_around(wrap_new, tgt_pos, wrap_new[0], 'x-')
        elif tgt_pos[1] > face_limits[tgt_pos[2]]["max_y"]:
            wrap_new = wrap[position[2]]['y+']
            dirct = wrap_new[2]
            tgt_pos = wrap_around(wrap_new, tgt_pos, wrap_new[0], 'y+')
        elif tgt_pos[1] < face_limits[tgt_pos[2]]["min_y"]:
            wrap_new = wrap[position[2]]['y-']
            dirct = wrap_new[2]
            tgt_pos = wrap_around(wrap_new, tgt_pos, wrap_new[0], 'y-')
        if maze_pts[(tgt_pos[0], tgt_pos[1],)][0] == "#":
            return new_pos, new_direction
        new_pos = tgt_pos
        new_direction = dirct

    return new_pos, new_direction


def get_face_ranges(maze_data):
    face_counter = 1
    limits_face = {}
    new_face = True
    for pos in maze_data.keys():
        if not new_face:
            matching_face_found = False
            for x in limits_face.values():
                if pos[0] in range(x["min_x"], x["max_x"]+1) and pos[1] in range(x["min_y"], x["max_y"]+1):
                    matching_face_found = True
            if not matching_face_found:
                new_face = True
                face_counter += 1
        if new_face:
            limits_face[face_counter] = {}
            limits_face[face_counter]["min_x"] = pos[0]
            limits_face[face_counter]["min_y"] = pos[1]
            limits_face[face_counter]["max_x"] = pos[0] + range_square - 1
            limits_face[face_counter]["max_y"] = pos[1] + range_square - 1
            new_face = False

    return limits_face


if __name__ == '__main__':
    start_time = time.time()
    maze = utils.read_file_as_lines(sys.argv[1])
    Test = sys.argv[1].startswith("Test")
    instructions = maze[-1]
    instructions = [x for x in re.split('(\d+)', instructions.strip()) if x != ""]
    maze = maze[0:-2]
    dim_x, dim_y = max([len(x) for x in maze]), len(maze)
    maze_pts = dict()
    curr_pos = None
    range_square = 4 if Test else 50
    for y in range(dim_y):
        for x in range(len(maze[y])):
            if maze[y][x] != " ":
                maze_pts[(x, y,)] = (maze[y][x],)
                if not curr_pos:
                    curr_pos = (x, y, 1, )
    face_limits = get_face_ranges(maze_pts)

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
    if Test:
        assert score == 6032
    print(f"pt1 solution: {score.real} time overall: {stop_time - start_time}")
    score = move_maze(curr_pos, instructions, True)
    if Test:
        assert score == 5031
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
