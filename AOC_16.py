import utils
import sys
import re
import numpy
import math


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
    dim = len(data)
    valves = [x[0] for x in data]
    shortest_paths = numpy.full((dim, dim), math.inf)
    rel_valves = []
    zero_valves = []
    for j in range(dim):
        shortest_paths[j, j] = 0
        for i in range(len(data[j]) - 2):
            elem1, elem2 = valves.index(data[j][0]), valves.index(data[j][2 + i])
            shortest_paths[elem1, elem2] = 1
            shortest_paths[elem2, elem1] = 1
        # cache valve values
        if data[j][1] != "0":
            rel_valves.append(int(data[j][1]))
        else:
            zero_valves.append(j)

    shortest_paths = floyd_warshal(shortest_paths)

    # Remove all 0-valves => there is no need to actually visit a room with a 0-valve, we can just delete them from
    # the solution space, significantly reducing the complexity of the problem
    for valve in reversed(zero_valves):
        shortest_paths = numpy.delete(shortest_paths, valve, 0)
        shortest_paths = numpy.delete(shortest_paths, valve, 1)

    return shortest_paths, rel_valves


if __name__ == '__main__':
    re_vals = re.compile('[-\\d]+|[A-Z]{2,}')
    data = [re.findall(re_vals, line) for line in utils.read_file_as_lines(sys.argv[1])]
    pathlengths, valve_vals = reduce_dimensionsality(data)
