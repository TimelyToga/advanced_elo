from collections import defaultdict

import sys
import math

BASE_SCORE = 2000.0
K = 20.0
NORMALIZING_FACTOR = 400.0

def get_player(players, id):
    if id not in players:
        players[id] = BASE_SCORE

    return players[id]

def calc_expectation(elo_a, elo_b):
    return 1 / (1 + 10**((elo_b - elo_a) / NORMALIZING_FACTOR))

def calc_new_elo(old_elo, score_difference, win, expectation):
    k_d = math.sqrt(abs(score_difference))
    return old_elo + k_d * K * (float(win) - expectation)

def main():
    if len(sys.argv) != 3: 
        print("Not enough arguments\n\nUsage: python elo.py <game_record_file> <player_names>")
        sys.exit(1)

    # Read in data file
    with open(sys.argv[1], 'r') as i:
        data = i.readlines()

    with open(sys.argv[2], 'r') as p:
        player_names_data = p.readlines()

    player_names = defaultdict()

    print("Processing matches...")
    for line in player_names_data:
        if(line != "\n"):
            line = line.split(":")
            player_names[line[1].rstrip()] = line[0]

    players = {}

    for line in data:
        line = line.split("\n")[0]
        entries = line.split(" ")

        w_elo = get_player(players, entries[0])
        l_elo = get_player(players, entries[1])

        e_a = calc_expectation(w_elo, l_elo)
        e_b = calc_expectation(l_elo, w_elo)

        sd = int(entries[2]) - int(entries[3])
        if(sd <= 0):
            print("InputError! Input data cannot contain draws or matches where winner score < loser score")
            print(line)
            continue

        ra_new = calc_new_elo(w_elo, sd, True, e_a)
        rb_new = calc_new_elo(l_elo, sd, False, e_b)

        players[entries[0]] = ra_new
        players[entries[1]] = rb_new
    
    print("\nSuccessfully processed {} matches between {} players\n".format(len(data), len(players.keys())))
    final_list = []
    for player, elo in players.iteritems():
        final_list.append((player_names[player], elo))

    final_list = sorted(final_list, key=lambda x: -x[1])

    for player in final_list:
        print("{}\t\t{}".format(player[0], player[1]))

if __name__ == "__main__":
    main()
