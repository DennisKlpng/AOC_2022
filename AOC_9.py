import utils
import sys
import math


def ad_ceil(num):
    return math.ceil(num) if num >= 0 else math.floor(num)


elem_vectors = {"U": (0, 1,), "D": (0, -1,), "R": (1, 0,), "L": (-1, 0,)}


def move_head(moves_head):
    head_pos = (0, 0,)  # horizontal, vertical
    positions = []
    for move in moves_head:
        for i in range(int(move[1])):
            head_pos = (head_pos[0] + elem_vectors[move[0]][0], head_pos[1] + elem_vectors[move[0]][1],)
            positions.append(head_pos)
    return positions


def follow_knot(pos_knot):
    tail_pos = (0, 0, )
    positions = [tail_pos]
    for pos in pos_knot:
        hor_dist, ver_dist = pos[0] - tail_pos[0], pos[1] - tail_pos[1]
        if math.sqrt(hor_dist * hor_dist + ver_dist * ver_dist) > 1.5:
            tail_pos = (tail_pos[0] + ad_ceil(0.5 * hor_dist), tail_pos[1] + ad_ceil(0.5 * ver_dist),)
            positions.append(tail_pos)
    return positions


if __name__ == '__main__':
    moves = [line.split(" ") for line in utils.read_file_as_lines(sys.argv[1])]
    head_moves = move_head(moves)

    for knot in range(9):
        head_moves = follow_knot(head_moves)
        if knot == 0:
            print("Solution pt1: " + str(len(set(head_moves))))
    print("Solution pt2: " + str(len(set(head_moves))))

