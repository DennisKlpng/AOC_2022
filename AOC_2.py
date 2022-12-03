import sys

rules_losing = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}
inverted_rules = {v: k for k, v in rules_losing.items()}

scores = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

subs = {"A": "rock", "B": "paper", "C": "scissors", "X": "rock", "Y": "paper", "Z": "scissors"}


def calc_result(opponent, player):
    score = scores[player]
    if player in rules_losing[opponent]:
        return score + 6
    elif opponent in rules_losing[player]:
        return score
    return score + 3


def cal_result_predefined(opponent, desired_result):
    if desired_result == "Y":  # draw
        return scores[opponent] + 3
    elif desired_result == "Z":  # win
        return scores[rules_losing[opponent]] + 6
    else:  # lose
        return scores[inverted_rules[opponent]]


if __name__ == '__main__':
    with open(sys.argv[1], "r") as f:
        moves = [move.split(" ") for move in f.read().splitlines()]
        score_naive = sum([calc_result(subs[move[0]], subs[move[1]]) for move in moves])
        print("Solution pt 1: " + str(score_naive))
        score_predefined = sum([cal_result_predefined(subs[move[0]], move[1]) for move in moves])
        print("Solution pt 2: " + str(score_predefined))
