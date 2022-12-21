import utils
import sys
import time
import math
import re
import operator


operators = {"+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}


def calc(ops, name):
    if ops[name].isdigit():
        return int(ops[name])
    num1, op, num2 = ops[name].split()
    return int(operators[op.strip()](calc(ops, num1), calc(ops, num2)))


if __name__ == '__main__':
    start_time = time.time()
    op_data = dict()
    for line in utils.read_file_as_lines(sys.argv[1]):
        name_field, oprt = line.split(": ")
        op_data[name_field] = oprt
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    score = calc(op_data, "root")
    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == 152
    print(f"pt1 solution: {score} time overall: {stop_time - start_time}")

    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
