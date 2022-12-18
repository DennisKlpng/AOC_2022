import utils
import sys
import time
import numpy


if __name__ == '__main__':
    start_time = time.time()
    data = [utils.extract_int_list_from_string(x) for x in utils.read_file_as_lines(sys.argv[1])]
    dim = max(max(pixel) for pixel in data)
    lava = numpy.full((dim+2, dim+2, dim+2), False, bool)
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
    #
    # stop_time = time.time()
    # print(f"pt2 solution: {} time overall: {stop_time - start_time}")
