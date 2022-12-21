import utils
import sys
import time
import operator


operators = {"+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul, "=": operator.eq}


def calc(ops, name, pt2=False, val=0):
    if ops[name].isdigit() or ops[name] == "1j":
        return complex(ops[name]), 0
    num1, op, num2 = ops[name].split()
    if pt2:
        ops["humn"] = "1j"
        num1, op, num2 = ops[name].split()
    v1, d1 = calc(ops, num1)
    v2, d2 = calc(ops, num2)
    new_val = complex(operators[op.strip()](v1, v2))
    return new_val, v1-v2


if __name__ == '__main__':
    start_time = time.time()
    op_data = dict()
    for line in utils.read_file_as_lines(sys.argv[1]):
        name_field, oprt = line.split(": ")
        op_data[name_field] = oprt
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time
    score, diff = calc(op_data, "root")
    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == 152
    print(f"Test: {operator.eq(4, 1)}")
    print(f"pt1 solution: {score.real} time overall: {stop_time - start_time}")
    start_val = 0
    # diff with using complex numbers as the human input immediately gives the relation between the actual diff and
    # the human influence on it
    score, diff = calc(op_data, "root", True, start_val)
    start_new = int(abs(diff.real / diff.imag))

    if sys.argv[1].startswith("Test"):
        assert start_new == 301
    stop_time = time.time()
    print(f"pt2 solution: {start_new} time overall: {stop_time - start_time}")
