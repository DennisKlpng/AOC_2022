import utils
import sys
import ast


def compare(a, b):
    if type(a) == type(b) and type(a) == int:
        return 0 if a == b else a < b
    elif type(a) == type(b) and type(a) == list:
        if len(a) == 0 and len(b) == 0:
            return 0
        elif len(a) == 0:
            return True
        elif len(b) == 0:
            return False
        val = compare(a[0], b[0])
        return val if type(val) == bool else compare(a[1:], b[1:])

    return compare([a], b) if type(a) == int else compare(a, [b])
    

if __name__ == '__main__':
    data = utils.split_fileinput_by_emptylines(sys.argv[1])
    print(f"Pt 1: {sum([x for x, val in enumerate(data, start=1) if compare(ast.literal_eval(val[0]), ast.literal_eval(val[1])) == True])}")
