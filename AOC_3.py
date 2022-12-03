import sys


def get_priority_sum_from_items(item_input):
    # uppercase letter ords are 65-90, lowercase 97-122
    priorities = [(number - 96) if number > 96 else (number - 38) for number in [ord(item) for item in item_input]]
    return str(sum(priorities))


if __name__ == '__main__':
    with open(sys.argv[1], "r") as f:
        rucksacks = f.read().splitlines()
        item_compartments = [[list(items[:len(items)//2]), list(items[len(items)//2:])] for items in rucksacks]
        intersections = [list(set(comp[0]).intersection(comp[1]))[0] for comp in item_compartments]

        print("Solution pt1: " + get_priority_sum_from_items(intersections))
        intersections_gr = [list(set(rucksacks[3*i]).intersection(rucksacks[3*i+1], rucksacks[3*i+2]))[0] for i in range(len(rucksacks)//3)]
        print("Solution pt2: " + get_priority_sum_from_items(intersections_gr))

