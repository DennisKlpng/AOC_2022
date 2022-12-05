import sys


if __name__ == '__main__':
    with open(sys.argv[1], "r") as f:
        pairs = [[list(range(int(er.split("-")[0]), int(er.split("-")[1])+1)) for er in line.split(",")] for line in
                 f.read().splitlines()]
        red = ["f" for pair in pairs if sorted(list(set(pair[0]).intersection(pair[1]))) in [pair[0], pair[1]]]
        print("solution pt 1: " + str(len(red)))
        over = ["f" for pair in pairs if len(list(set(pair[0]).intersection(pair[1]))) > 0]
        print("solution p1 2: " + str(len(over)))
