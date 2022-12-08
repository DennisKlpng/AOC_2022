import utils
import sys


if __name__ == '__main__':
    trees = [[int(line[i]) for i in range(len(line))] for line in utils.read_file_as_lines(sys.argv[1])]
    visible = 0
    max_trees = 0
    for i in range(len(trees)):
        for j in range(len(trees[i])):
            val = trees[i][j]
            col = [trees[x][j] for x in range(len(trees))]
            visible += all(x < val for x in trees[i][:j]) or all(x < val for x in trees[i][j + 1:]) \
                       or all(x < val for x in col[:i]) or all(x < val for x in col[i + 1:])
            if j in [0, len(trees[i])-1] or i in [0, len(col)-1]:
                continue

            # slices, won't go out of bounds since we skip border trees (as they always have 0 score):
            tr_lft = trees[i][j-1::-1]  # to the left
            tr_rgt = trees[i][j + 1:]  # to the right
            tr_up = col[i-1::-1]  # to the top
            tr_down = col[i+1:]  # to the bottom

            # offset by one to always include found element
            def num(lst): return next((x for x in range(1, len(lst) + 1) if lst[x - 1] >= val), len(lst))
            max_trees = max(max_trees, num(tr_lft) * num(tr_rgt) * num(tr_up) * num(tr_down))

    print("solution pt 1: " + str(visible))
    print("solution pt 2: " + str(max_trees))
