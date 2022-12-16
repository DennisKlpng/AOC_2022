import utils
import sys
import re
import numpy
import math
from copy import deepcopy
import time


def floyd_warshal(matrix):
    dim = len(matrix)
    # Using floyd-warshall algorithm to calculate the distances between all valves
    for k in range(dim):
        for i in range(dim):
            for j in range(dim):
                if matrix[i, j] > matrix[i, k] + matrix[k, j]:
                    matrix[i, j] = matrix[i, k] + matrix[k, j]
                    matrix[j, i] = matrix[i, j]
    return matrix


# returns: matrix of all travel costs (symmetrical), list of valve values with same indexing as the matrix
def reduce_dimensionsality(input_data):
    dim = len(input_data)
    valves = [x[0] for x in input_data]
    shortest_paths = numpy.full((dim, dim), math.inf)
    rel_valves = []
    zero_valves = []
    for j in range(dim):
        shortest_paths[j, j] = 0
        for i in range(len(input_data[j]) - 2):
            elem1, elem2 = valves.index(input_data[j][0]), valves.index(input_data[j][2 + i])
            shortest_paths[elem1, elem2] = 1
            shortest_paths[elem2, elem1] = 1
        # cache valve values
        if input_data[j][1] != "0" or input_data[j][0] == "AA":
            rel_valves.append(int(input_data[j][1]))
        else:
            zero_valves.append(j)

    shortest_paths = floyd_warshal(shortest_paths)

    # Remove all 0-valves => there is no need to actually visit a room with a 0-valve, we can just delete them from
    # the solution space, significantly reducing the complexity of the problem
    for valve in reversed(zero_valves):
        shortest_paths = numpy.delete(shortest_paths, valve, 0)
        shortest_paths = numpy.delete(shortest_paths, valve, 1)

    return shortest_paths, rel_valves


def solver(pathlengths, vals, start_index, rem_time, pt2=False):
    def get_all_paths(rem_t, start_in):
        all_paths = []
        all_pressures = []
        stack = [(rem_time, start_in, [start_in], [], 0)]  # ., ., visited, rates, pressure released
        while stack:
            rt, st_in, path, rates, p = stack.pop()
            stack_new = []
            for ind in range(len(vals)):
                if ind in path or ind == start_in:  # never visit previously visited again
                    continue
                dt = 1 + pathlengths[st_in, ind]  # time to reach and open that valve
                if rt - dt <= 0:  # not enough time to open valve
                    continue
                p_new = p + sum(rates) * dt
                elem = rt - dt, ind, path + [ind], rates + [vals[ind]], p_new
                stack_new.append(elem)
            if stack_new:
                stack.extend(stack_new)
            else:
                all_paths.append(path)
                all_pressures.append(p + rt*sum(rates))

        return all_paths, all_pressures
    pths, press = get_all_paths(rem_time, start_index)
    if not pt2:
        return max(press)
    # Part 2: paths that intersect will certainly not be the correct ones


if __name__ == '__main__':
    start_time = time.time()
    re_vals = re.compile('[-\\d]+|[A-Z]{2,}')
    data = [re.findall(re_vals, line) for line in utils.read_file_as_lines(sys.argv[1])]
    distances, valve_values = reduce_dimensionsality(data)
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    pt1 = solver(distances, valve_values, valve_values.index(0), 30)
    stop_time = time.time()
    print(f"pt1 solution: {pt1}  time: {stop_time - start_time}")
    start_time = stop_time
    pt2 = solver(distances, valve_values, valve_values.index(0), 26, True)
    stop_time = time.time()
    print(f"pt2 solution: {pt2} time: {stop_time - start_time}")
