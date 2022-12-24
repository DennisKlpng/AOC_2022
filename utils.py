import re

def split_fileinput_by_emptylines(filename):  # empty line separated blocks
    with open(filename, "r") as f:
        data = f.read().split("\n\n")
        return [[elem for elem in chunk.splitlines()] for chunk in data]


def read_file_as_chunk(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def read_file_as_lines(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


def extract_int_list_from_string(input_str):  # whitespace separated elements
    re_num = re.compile('[-\\d]+')
    return [int(x) for x in re.findall(re_num, input_str)]


def extract_float_list_from_string(input_str, decimal_sep):  # whitespace separated elements
    re_num = re.compile(f'[-{decimal_sep}\\d]+')
    return [float(x) for x in re.findall(re_num, input_str)]


def get_neighbours(coord):
    row, col = coord[0], coord[1]
    return [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]


def get_diagneighbours(coord):
    row, col = coord[0], coord[1]
    return [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1),
            (row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]


def get_neighbours_3d(p):
    return [(p[0] + dx, p[1] + dy, p[2] + dz,) for (dx, dy, dz) in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]


class GenericTree(object):
    def __init__(self, name='root', size=None, is_file=False):
        self.name = name
        self.parent = None
        self.size = size
        self.is_file = is_file
        self.children = []

    def add_child(self, name, size=None, is_file=False):
        self.children.append(GenericTree(name, size, is_file))
        self.children[-1].parent = self

    def get_parent(self):
        return self.parent

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def fill_node_sizes(self):
        size = 0 if self.size is None else self.size
        for child in self.children:
            size += child.fill_node_sizes()
        if self.size is None:
            self.size = size
        return size
