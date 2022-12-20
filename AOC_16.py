import utils
import sys
import re
import numpy
import math
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
        stack = [(rem_time, start_in, [start_in], 0)]  # ., ., visited, pressure released
        while stack:
            rt, st_in, path, p = stack.pop()
            rate_sum = sum([vals[x] for x in path])
            if pt2 and len(path) > len(vals)*0.5 and p > 0:
                all_paths.append(path[1:])
                all_pressures.append(p + rt * rate_sum)
            stack_new = []
            for ind in range(len(vals)):
                if ind in path or ind == start_in:  # never visit previously visited again
                    continue
                dt = 1 + pathlengths[st_in, ind]  # time to reach and open that valve
                if rt - dt <= 0:  # not enough time to open valve
                    continue
                p_new = p + rate_sum * dt
                elem = rt - dt, ind, path + [ind], p_new
                stack_new.append(elem)
            if stack_new:
                stack.extend(stack_new)
            else:
                all_paths.append(path[1:])
                all_pressures.append(p + rt*rate_sum)

        return all_pressures, all_paths
    press, pths = get_all_paths(rem_time, start_index)
    if not pt2:
        return max(press)
    press, pths = zip(*sorted(zip(press, pths), reverse=True))

    print(f"Comppressing lists, len: {len(pths)}")

    def compress_lists(l_pths):
        # Compress list of paths (by factor ~10) by getting the indices of the path-permutation with the highest
        # pressure. As e.g. [1, 3, 4] and [1, 4, 3] visit the same valves, it doesn't make much sense to consider both
        # for the O(N²) comparison that follow beneath. This trick made the numbers actually manageable
        ids_unq_paths = []
        set_paths = set()
        for id in range(len(l_pths)):
            if tuple(sorted(l_pths[id])) not in set_paths:
                set_paths.add(tuple(sorted(l_pths[id])))
                ids_unq_paths.append(id)
        return ids_unq_paths

    unq_paths_list = compress_lists(pths)
    print(f"Comparing lists, len: {len(unq_paths_list)}")
    max_pressure = 0
    # Part 2: paths that overlap (aka elephant will turn the same valves) will certainly not be the correct ones
    for i in range(0, len(unq_paths_list)):
        max_val_ele = press[unq_paths_list[i + 1]]
        if press[unq_paths_list[i]] + max_val_ele < max_pressure:
            break  # since vals are sorted, max can't be exceeded anymore
        for j in range(i + 1, len(unq_paths_list)):
            if not set(pths[unq_paths_list[i]]).isdisjoint(set(pths[unq_paths_list[j]])):
                continue
            new_max = press[unq_paths_list[i]] + press[unq_paths_list[j]]
            if new_max > max_pressure:
                max_pressure = new_max
                break
    return max_pressure


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
