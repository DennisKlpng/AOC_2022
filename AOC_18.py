import utils
import sys
import time
import numpy
from itertools import combinations


if __name__ == '__main__':
    start_time = time.time()
    data = [utils.extract_int_list_from_string(x) for x in utils.read_file_as_lines(sys.argv[1])]
    dim = max(max(pixel) for pixel in data)
    lava = numpy.full((dim+1, dim+1, dim+1), False, bool)
    for pixel in data:
        lava[tuple(pixel)] = True
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    sides_sum = sum(numpy.sum(numpy.diff(lava, 1, axis, False, False)) for axis in [0, 1, 2])
    stop_time = time.time()
    assert sides_sum == 3346 if sys.argv[1].startswith("Data") else sides_sum == 64
    print(f"pt1 solution: {sides_sum} time overall: {stop_time - start_time}")
    start_time = stop_time

    visited = set()
    stack = [(0, 0, 0,)]
    open_air = numpy.full((dim+1, dim+1, dim+1), False, bool)
    while stack:
        p = stack.pop()
        neighbours = utils.get_neighbours_3d(p)
        for nb in neighbours:
            if any(nb[x] < 0 or nb[x] > dim for x in [0, 1, 2]):
                continue
            if nb not in visited and not lava[nb]:
                stack.append(nb)
                visited.add(nb)
                open_air[nb] = True
    # Replace all non exposed air squares with lava (finding by comparing the matrix of exposed with all air)
    lava = numpy.where(numpy.equal(open_air, lava), True, lava)

    sides_sum = sum(numpy.sum(numpy.diff(lava, 1, axis, False, False)) for axis in [0, 1, 2])
    stop_time = time.time()
    print(f"pt2 solution: {sides_sum} time overall: {stop_time - start_time}")
