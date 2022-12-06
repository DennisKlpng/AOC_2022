import utils
import sys
from collections import deque
import re
import copy


def get_nth_unique(input_string, character):
    lst_input = list(input_string)
    for i in range(character-1, len(input_string)):
        if len(lst_input[i-(character-1):i+1]) == len(set(lst_input[i-(character-1):i+1])):
            return i+1


if __name__ == '__main__':
    data_string = utils.read_file_as_chunk(sys.argv[1])

    print("Test 1: " + str(get_nth_unique("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4)))
    print("Test 2: " + str(get_nth_unique("bvwbjplbgvbhsrlpgdmjqwftvncz", 4)))
    print("Test 3: " + str(get_nth_unique("nppdvjthqldpwncqszvftbrmjlhg", 4)))
    print("Test 4: " + str(get_nth_unique("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4)))
    print("Test 5: " + str(get_nth_unique("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4)))

    print("Sol pt 1: " + str(get_nth_unique(data_string, 4)))

    print("Test 1b: " + str(get_nth_unique("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14)))
    print("Test 2b: " + str(get_nth_unique("bvwbjplbgvbhsrlpgdmjqwftvncz", 14)))
    print("Test 3b: " + str(get_nth_unique("nppdvjthqldpwncqszvftbrmjlhg", 14)))
    print("Test 4b: " + str(get_nth_unique("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14)))
    print("Test 5b: " + str(get_nth_unique("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14)))

    print("Sol pt 1b: " + str(get_nth_unique(data_string, 14)))


