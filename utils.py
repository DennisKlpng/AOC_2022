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
    return[int(elem) for elem in input_str.strip().split(" ") if elem[0].isdigit()]


def extract_float_list_from_string(input_str):  # whitespace separated elements
    return[float(elem) for elem in input_str.strip().split(" ") if elem[0].isdigit()]


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
