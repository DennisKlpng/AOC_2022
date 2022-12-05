import utils
import sys
from collections import deque
import re
import copy


def print_top_queues(queuelist):
    str_result = ""
    for q in queuelist:
        if q:
            str_result += q[-1]
        else:
            str_result += "#"
    print(str_result)


def move_operation(op_list, queuelist, keep_order):
    for line in op_list:  # parse instructions
        num_moves, base, tgt = utils.extract_int_list_from_string(line)
        for i in range(num_moves):
            if not keep_order:
                queuelist[tgt-1].append(queuelist[base-1].pop())
            else:
                pos_insert = len(queuelist[tgt-1])-i
                queuelist[tgt-1].insert(pos_insert, queuelist[base-1].pop())


if __name__ == '__main__':
    data = utils.split_fileinput_by_emptylines(sys.argv[1])

    queues = []
    for line in data[0]:  # get num of queues
        if line.strip()[0].isdigit():
            elems = line.strip().split(" ")
            for i in range(int(elems[len(elems)-1])):
                queues.append(deque())

    for line in data[0]:  # fill queues
        for m in re.finditer(']', line):
            index = int((m.start()-2)/4)
            queues[index].appendleft(line[m.start()-1])

    queues_pt2 = copy.deepcopy(queues)
    move_operation(data[1], queues, False)
    print("Pt 1 solution:")
    print_top_queues(queues)
    move_operation(data[1], queues_pt2, True)
    print("Pt 2 solution:")
    print_top_queues(queues_pt2)
