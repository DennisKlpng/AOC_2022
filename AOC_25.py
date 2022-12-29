import utils
import sys
import time
from math import log

snafu_nums = {"0": 0, "1": 1, "2": 2, "=": -2, "-": -1}
snafu_inv = {v: k for k, v in snafu_nums.items()}


def convert_to_dec(snafu):
    num_digits = len(snafu)
    dec_num = 0
    for i in range(num_digits):
        dec_num += pow(5, num_digits - i - 1) * snafu_nums[snafu[i]]
    return dec_num


def convert_to_snafu(dec):
    snafu = ""
    num_dgts = int(log(dec, 5))
    for i in range(num_dgts, -1, -1):
        dgt = round(dec/pow(5, i))
        snafu += snafu_inv[dgt]
        dec -= dgt * pow(5, i)
    return snafu


if __name__ == '__main__':
    start_time = time.time()
    nums = utils.read_file_as_lines(sys.argv[1])

    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")
    start_time = stop_time

    sum_nums = 0
    for number in nums:
        sum_nums += convert_to_dec(number)

    score = convert_to_snafu(sum_nums)
    stop_time = time.time()
    if sys.argv[1].startswith("Test"):
        assert score == "2=-1=0"
    print(f"pt1 solution: {score} time overall: {stop_time - start_time}")