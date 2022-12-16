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


def solver(pathlenghts, vals, start_index, rem_time, pt2=False):
    stack = [(rem_time, start_index, [start_index], [], 0,)]  # ., ., visited, rates, pressure released
    max_press = 0
    while stack:
        s = stack.pop()
        if s[0] <= 0:  # no time left
            continue
        pot_p = sum(s[3]) * s[0]  # pot release w/o moves: rate_sum * remaining time
        if (s[4] + pot_p) > max_press:
            max_press = s[4] + pot_p
        theoretical_p = s[0] * sum([r for r in vals if r not in s[2]])
        if (theoretical_p + pot_p + s[4]) < max_press:  # throw away all solutions that can't possibly beat the max
            continue
        for ind in range(len(vals)):
            if ind in s[2] or ind == start_index:  # never visit previously visited again
                continue
            dt = 1 + pathlengths[s[1], ind]  # time to reach and open that valve
            p = s[4] + sum(s[3])*dt  # new pressure released: old p + sum of all rates * time_diff since old p
            v = deepcopy(s[2])
            r = deepcopy(s[3])
            v.append(ind)
            r.append(vals[ind])
            stack.append((int(s[0] - dt), ind, v, r, p,))
    return int(max_press)


if __name__ == '__main__':
    start_time = time.time()
    re_vals = re.compile('[-\\d]+|[A-Z]{2,}')
    data = [re.findall(re_vals, line) for line in utils.read_file_as_lines(sys.argv[1])]
    pathlengths, valve_vals = reduce_dimensionsality(data)
    print(f"pt1: {solver(pathlengths, valve_vals, valve_vals.index(0), 30)}")
    stop_time = time.time()
    print(f"pt1 time: {stop_time - start_time}")
