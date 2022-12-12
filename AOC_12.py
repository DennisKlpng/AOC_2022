import utils
import sys
import numpy as np


def bfs(in_mat, shortest=False):
    visited = set()
    search = np.where(in_mat == 27)
    dim_lines, dim_cols = in_mat.shape
    queue = [(search[0][0], search[1][0],)]
    counters = np.zeros(shape=in_mat.shape, dtype=int)

    while queue:
        elem = queue.pop(0)
        neighbors = utils.get_neighbours(elem)
        for neighbor in neighbors:
            if 0 <= neighbor[0] < dim_lines and 0 <= neighbor[1] < dim_cols and in_mat[elem] - in_mat[neighbor] <= 1 \
                    and neighbor not in visited:
                if in_mat[neighbor] == 1 and shortest:
                    return counters[elem] + 1
                elif in_mat[neighbor] == 0:
                    return counters[elem] + 1
                queue.append(neighbor)
                visited.add(neighbor)
                counters[neighbor] = counters[elem] + 1


if __name__ == '__main__':
    # uppercase letter ords are 65-90 => E = 69, S = 83, lowercase 97-122. Target: S = 0, intermediates 1-26, E = 27
    def ord_val(x): return 0 if x == 'S' else (27 if x == 'E' else ord(x) - 96)
    # lines, columns!
    matrix = np.array([[ord_val(field) for field in list(line)] for line in utils.read_file_as_lines(sys.argv[1])])

    print(f"Solution pt 1: {bfs(matrix)}")
    print(f"Solution pt 2: {bfs(matrix, True)}")
