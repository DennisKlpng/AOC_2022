import utils
import sys
import time
import math
from collections import deque


if __name__ == '__main__':
    start_time = time.time()
    nums = list(enumerate([int(x) for x in utils.read_file_as_lines(sys.argv[1])]))
    nums_orig = tuple(nums)
    nums = deque(nums)

    nums_pt2 = [(x[0], x[1]*811589153) for x in nums]
    nums_orig_pt2 = tuple(nums_pt2)
    nums_pt2 = deque(nums_pt2)
    stop_time = time.time()
    print(f"Initialization time: {stop_time - start_time} seconds")

    start_time = stop_time
    for i in range(len(nums)):
        index = nums.index(nums_orig[i])
        nums.remove(nums_orig[i])
        nums.rotate(-nums_orig[i][1])
        nums.insert(index, nums_orig[i])
    nums = [x[1] for x in nums]
    start_index = nums.index(0)
    score = sum([nums[(start_index + 1000*i) % len(nums)] for i in [1, 2, 3]])
    stop_time = time.time()
    assert score == 3 if sys.argv[1].startswith("Test") else 1349
    print(f"pt1 solution: {score} time overall: {stop_time - start_time}")

    for j in range(10):
        for i in range(len(nums_pt2)):
            index = nums_pt2.index(nums_orig_pt2[i])
            nums_pt2.remove(nums_orig_pt2[i])
            nums_pt2.rotate(-nums_orig_pt2[i][1])
            nums_pt2.insert(index, nums_orig_pt2[i])
    nums_pt2 = [x[1] for x in nums_pt2]
    start_index = nums_pt2.index(0)
    score = sum([nums_pt2[(start_index + 1000 * i) % len(nums_pt2)] for i in [1, 2, 3]])
    stop_time = time.time()
    print(f"pt2 solution: {score} time overall: {stop_time - start_time}")
