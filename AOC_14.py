import utils
import sys
from collections import defaultdict
from numpy import sign


def get_limits(val_list):  # max_r, min_r, max_i, min_i
    val_real = [key.real for key in val_list]
    val_imag = [key.imag for key in val_list]
    return [int(max(val_real)), int(min(val_real)), int(max(val_imag)), int(min(val_imag))]


def vis(world_dict, lim):
    for row in range(lim[3], lim[2]+1):
        print([world_dict[dr + row*1j] for dr in range(lim[1], lim[0]+1)])
    print(" ")


def sand_move(pos, world_dict, lowest_rock):
    #print(f"Trying to fall down from pos: {pos}")
    #print(f"Below at pos {pos + 1j} is {world_dict[pos + 1j]}")
    if pos.imag > lowest_rock:
        return False, pos
    # try to move one tile down
    if world_dict[pos + 1j] == '.':
        return sand_move(pos + 1j, world_dict, lowest_rock)
    # else down and left
    elif world_dict[pos - 1 + 1j] == '.':
        return sand_move(pos - 1 + 1j, world_dict, lowest_rock)
    # else down and right
    elif world_dict[pos + 1 + 1j] == '.':
        return sand_move(pos + 1 + 1j, world_dict, lowest_rock)
    # no way down, not in the abyss: very fine to place sand
    return True, pos


if __name__ == '__main__':
    # complex.real = distance_right, complex.imag = distance_down
    data = [[complex(int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in line.split(' -> ')]
            for line in utils.read_file_as_lines(sys.argv[1])]
    world = defaultdict(lambda: '.')
    for path in data:
        for line_s, line_e in zip(path[:-1], path[1:]):
            diff = line_e - line_s
            diff_r, diff_i = int(diff.real), int(diff.imag)
            if diff_r != 0:
                # e.g. 0 .. 4 => range(0, 5, 1) => vals 0, .., 4; likewise 0 .. -4 => range(0, -5, -1)
                for i in range(0, diff_r+sign(diff_r), sign(diff_r)):
                    world[line_s + i] = '#'
            if diff_i != 0:
                for i in range(0, diff_i+sign(diff_i), sign(diff_i)):
                    world[line_s + i*1j] = '#'
    world[500 + 0j] = '+'
    limits = get_limits(world)
    print(limits)
    # vis(world, limits)  # debug, initial state

    sand_counter = 0
    while True:
        nom, pos = sand_move(500 + 0j, world, limits[2])
        if nom is True:
            world[pos] = 'o'
            sand_counter += 1
            # vis(world, limits)  # debug vi
        else:
            break
    print(f"Sol pt 1: {sand_counter}")
