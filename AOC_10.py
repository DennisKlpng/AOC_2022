import utils
import sys
import math
import os


if __name__ == '__main__':
    tgt_vals = []
    tgt_cycles = [20, 60, 100, 140, 180, 220]
    counter, complete_cycles, curr_val = 1, 0, 1
    instructions = utils.read_file_as_lines(sys.argv[1])
    skip_read = False
    tgt_symbols = [["." for i in range(40)] for j in range(6)]
    os.system('color')
    for i in range(240):
        if len(tgt_cycles) > 0 and i+1 == tgt_cycles[0]:
            tgt_vals.append(curr_val*tgt_cycles.pop(0))
        if i % 40 in [curr_val-1, curr_val, curr_val+1]:
            tgt_symbols[math.floor(i/40)][i % 40] = '\x1b[6;30;42m' + '#' + '\x1b[0m'
        if not skip_read:
            if instructions[0] != "noop":
                counter += int(instructions[0].split(" ")[1])
                skip_read = True
            instructions.pop(0)
        else:
            curr_val = counter
            skip_read = False
    print(f"Pt 1 solution: {str(sum(tgt_vals))}")
    print('\n'.join([''.join([str(cell) for cell in row]) for row in tgt_symbols]))
