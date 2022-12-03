import sys


if __name__ == '__main__':
    with open(sys.argv[1], "r") as f:
        calories = [[int(cal_val) for cal_val in block.splitlines()] for block in f.read().split("\n\n")]
        cal_sums_sorted = sorted([sum(foods) for foods in calories], reverse=True)
        print("Solution pt 1: " + str(cal_sums_sorted[0]))
        print("Solution pt 2: " + str(cal_sums_sorted[0] + cal_sums_sorted[1] + cal_sums_sorted[2]))
