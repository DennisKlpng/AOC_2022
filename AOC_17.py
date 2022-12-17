import utils
import sys
import re
import numpy
import math
import time


def get_rock(h, cycle):
    m = cycle % 5
    a = 2 + 1j
    h += 4
    if m == 0:
        return {2 + h * 1j, 3 + h * 1j, 4 + h * 1j, 5 + h * 1j}
    elif m == 1:
        return {3 + h * 1j, 2 + (h+1) * 1j, 3 + (h+1) * 1j, 4 + (h+1) * 1j, 3 + (h+2) * 1j}
    elif m == 2:
        return {2 + h * 1j, 3 + h * 1j, 4 + h * 1j, 4 + (h+1) * 1j, 4 + (h+2) * 1j}
    elif m == 3:
        return {2 + h * 1j, 2 + (h+1) * 1j, 2 + (h+2) * 1j, 2 + (h+3) * 1j}
    elif m == 4:
        return {2 + h * 1j, 3 + h * 1j, 2 + (h+1) * 1j, 3 + (h+1) * 1j}


def move_rock_left(rock):
    if any([x.real == 0 for x in list(rock)]):
        return rock
    return set([complex(x. real - 1, x.imag) for x in list(rock)])


def move_rock_right(rock):
    if any([x.real == 6 for x in list(rock)]):
        return rock
    return set([complex(x. real + 1, x.imag) for x in list(rock)])


def move_rock_down(rock):
    return set([complex(x.real, x.imag - 1) for x in list(rock)])


def visualize_trench(trench, max_height):
    numpy.set_printoptions(threshold=sys.maxsize)
    vis = numpy.full((int(max_height) + 1, 7), 1)
    for occ in trench:
        vis[int(occ.imag), int(occ.real)] = 8
    print(numpy.flipud(vis))


if __name__ == '__main__':
    start_time = time.time()
    data = [-1 if x == "<" else 1 for x in list(utils.read_file_as_lines(sys.argv[1])[0])]
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    # Parsing starts at 0+1i => real from the left, imag from the bottom. 1i = 1str row
    start_time = stop_time
    height, moves = 0, 0
    occupied = set([x + 0j for x in range(7)])
    num_rocks_todo = 1000000000000
    tracked_cycle = []
    # cache = 50
    height_offset = 0
    det_loop = False
    i = 0
    while i < num_rocks_todo:
        new_rock = get_rock(height, i)
        while True:
            # move
            new_rock_tmp = move_rock_left(new_rock) if data[moves] == -1 else move_rock_right(new_rock)
            if not new_rock_tmp & occupied:
                new_rock = new_rock_tmp
            moves = (moves + 1) % len(data)
            new_rock_tmp = move_rock_down(new_rock)
            if not new_rock_tmp & occupied:
                new_rock = new_rock_tmp
            else:
                occupied.update(new_rock)
                height = max(height, max([x.imag for x in list(new_rock)]))
                break
        i += 1
        if i == 2021:
            stop_time = time.time()
            print(f"pt1 solution: {height}  time: {stop_time - start_time}")
            tracked_cycle = [i % 5, moves, height, i]
        if i > 2021:
            if i % 5 == tracked_cycle[0] and moves == tracked_cycle[1] and not det_loop:
                # loop detected
                dh = height - tracked_cycle[2]
                di = i - tracked_cycle[3]
                num_future_cycles = math.floor((num_rocks_todo - i)/di)
                i += di*num_future_cycles
                height_offset = dh*num_future_cycles
                det_loop = True

    stop_time = time.time()
    print(f"pt2 solution: {height + height_offset} time overall: {stop_time - start_time}")
