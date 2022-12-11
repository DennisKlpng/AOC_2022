import utils
import sys
import math
from functools import reduce
import re


regex_int = re.compile('[0-9]+')


class Monkey(object):
    def __init__(self, input_info):
        self.id = int(regex_int.findall(input_info[0].strip())[0])
        self.items = [int(x) for x in regex_int.findall(input_info[1].strip())]
        mod = input_info[2].strip().split('old ')[1]
        if mod[0] == '+':
            self.modify_stuff = lambda x: x + int(mod[2:])
        elif mod[2].isdigit():
            self.modify_stuff = lambda x: x * int(mod[2:])
        else:
            self.modify_stuff = lambda x: x * x
        self.conddiv = int(regex_int.findall(input_info[3].strip())[0])
        self.tgt_true = int(regex_int.findall(input_info[4].strip())[0])
        self.tgt_false = int(regex_int.findall(input_info[5].strip())[0])
        self.inspections = 0

    def shuffle_stuff(self):
        tgt_list = []
        for it in self.items:
            self.inspections += 1
            val = math.floor(self.modify_stuff(it) / 3)
            if val % self.conddiv == 0:
                tgt_list.append((val, self.tgt_true))
            else:
                tgt_list.append((val, self.tgt_false))
        self.items.clear()
        return tgt_list

    def append_item(self, val):
        self.items.append(val)


if __name__ == '__main__':
    input_information = utils.split_fileinput_by_emptylines(sys.argv[1])
    monkeys = [Monkey(line) for line in input_information]
    for i in range(20):
        for monkey in monkeys:
            items_exchange = monkey.shuffle_stuff()
            for item in items_exchange:
                monkeys[item[1]].append_item(item[0])
    print(f"Pt 1: {reduce(lambda x, y: x * y, sorted([monkey.inspections for monkey in monkeys], reverse=True)[0:2])}")
