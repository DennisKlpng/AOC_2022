import utils
import sys
from collections import deque
import re
import copy


def get_nodes_with_max_size(root, nodes, tgt, tgt_le=True):
    if root.size <= tgt and tgt_le and not root.is_file:
        nodes.append(root.size)
    elif root.size >= tgt and not tgt_le and not root.is_file:
        nodes.append(root.size)
    for child in root.children:
        get_nodes_with_max_size(child, nodes, tgt, tgt_le)


if __name__ == '__main__':
    data = utils.read_file_as_chunk(sys.argv[1]).splitlines()
    tree_root = utils.GenericTree('root')
    curr_node = None
    for line in data:
        if line[:4] == '$ cd':
            if line[5:].strip() == '/':
                curr_node = tree_root
            elif line[5:].strip() == '..':
                curr_node = curr_node.get_parent()
            else:
                curr_node = curr_node.get_child(line[5:].strip())
        elif line[:4] == 'dir ':
            curr_node.add_child(line[4:])
        elif line[0].isdigit():
            curr_node.add_child(line.split(' ')[1], int(line.split(' ')[0]), True)

    tree_root.fill_node_sizes()

    node_list = []
    get_nodes_with_max_size(tree_root, node_list, 100000)
    print("Pt1: " + str(sum(node_list)))

    space_needed_to_delete = tree_root.size - 40000000
    node_list_pt2 = []
    get_nodes_with_max_size(tree_root, node_list_pt2, space_needed_to_delete, False)
    print("Pt2: " + str(sorted(node_list_pt2)[0]))


