import utils
import sys
from itertools import chain


def check_line(line_num, sens_data):
    intersections = None
    blocked_pos = set()
    beacon_pos = set()
    for sens_info in sens_data:
        # manhattan distance
        dist = abs(sens_info[0] - sens_info[2]) + abs(sens_info[1] - sens_info[3])
        x_max_dist = dist - abs(sens_info[1] - line_num)
        if x_max_dist <= 0:  # beacon range doesn't intersect line
            continue
        min_x, max_x = sens_info[0] - x_max_dist, sens_info[0] + x_max_dist
        intersections = chain(intersections, range(min_x, max_x+1)) if intersections else range(min_x, max_x+1)
        if sens_info[3] == line_num:
            beacon_pos.add(sens_info[2])

    inter_list = set(intersections)
    inter_list = inter_list.symmetric_difference(beacon_pos)
    return len(inter_list)


def pt2(max_size, sens_info):
    # Reasoning for pt2: since there is a single free pt it must be directly adjacent to at least 2 of the sensor ranges
    # iterate through all sensors
    for sens in sens_info:
        # dist to elements just outside of range
        dist = abs(sens[0] - sens[2]) + abs(sens[1] - sens[3]) + 1
        pts = []
        # Iterate through all points just outside of sens
        for x in range(max(0, sens[0] - dist), min(max_size, sens[0] + dist)):
            mod = dist - abs(x - sens[0])
            for y in [sens[1] + mod, sens[1] - mod]:
                if 0 < y < max_size + 1:
                    # check if point is outside of ALL other sensor ranges, therefore iterate over all sensors again
                    for sens_comp in sens_info:
                        dist_comp = abs(sens_comp[0] - sens_comp[2]) + abs(sens_comp[1] - sens_comp[3])
                        dist_pt = abs(x - sens_comp[0]) + abs(y - sens_comp[1])
                        if dist_pt <= dist_comp:
                            # Point is in sens_comp => break
                            break
                    else:
                        # python insanity, aka else for for => only reached when loop didn't break
                        # only reached when no sensor broke the loop => this must be the solution
                        return x * 4000000 + y


if __name__ == '__main__':
    data = [utils.extract_int_list_from_string(line) for line in utils.read_file_as_lines(sys.argv[1])]
    print(f"Pt 1: {check_line(10, data) if sys.argv[1].startswith('Test') else check_line(2000000, data)}")
    print(f"Pt 2: {pt2(20, data) if sys.argv[1].startswith('Test') else pt2(4000000, data)}")
