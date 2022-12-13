from csv import excel_tab

import utils
import sys
from ast import literal_eval as leval
import functools


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


def evcomp(a, b): return -1 if compare(a, b) else 1


if __name__ == '__main__':
    data = utils.split_fileinput_by_emptylines(sys.argv[1])
    print(f"Pt 1: {sum([x for x, val in enumerate(data, start=1) if compare(leval(val[0]), leval(val[1])) == True])}")
    data_pt2 = [leval(x) for sublist in data for x in sublist]
    ex_0, ex_1 = [[2]], [[6]]
    data_pt2 += [ex_0, ex_1]
    data_pt2 = sorted(data_pt2, key=functools.cmp_to_key(evcomp))
    print(f"Pt 2: {(data_pt2.index(ex_0) + 1) * (data_pt2.index(ex_1) + 1)}")
