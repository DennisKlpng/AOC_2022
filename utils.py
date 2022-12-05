def split_fileinput_by_emptylines(filename):  # empty line separated blocks
    with open(filename, "r") as f:
        data = f.read().split("\n\n")
        return [[elem for elem in chunk.splitlines()] for chunk in data]


def extract_int_list_from_string(input_str):  # whitespace separated elements
    return[int(elem) for elem in input_str.strip().split(" ") if elem[0].isdigit()]


def extract_float_list_from_string(input_str):  # whitespace separated elements
    return[float(elem) for elem in input_str.strip().split(" ") if elem[0].isdigit()]