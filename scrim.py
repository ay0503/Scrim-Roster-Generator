from itertools import combinations, product
from user_data import *

DEBUG = False
USER_POOL = list(user_pool.values())
FIXES = {'DK_Showmaker': 'Mid',
         'LukeyParkey': 'Top',
         'dotoeri': 'Jungle',
         'Eightine': 'ADC',}

# generate possible position configs
def generate_position_permutations(team, players):
    player_positions = []
    # For each player, get a list of possible positions they can play
    for player_name in team:
        player = next((p for p in players if p.name == player_name), None)
        if player:
            player_positions.append(
                [(player_name, position.lane) for position in player.positions]
            )
    return list(product(*player_positions))


# calculate the balance score for a team composition
def calculate_team_score(team, players):
    team_score = Team()
    for player_name, position in team:
        player = next((p for p in players if p.name == player_name), None)
        if player:
            position_obj = next(
                (pos for pos in player.positions if pos.lane == position), None
            )
            if position_obj:
                team_score.laning_phase += (
                    position_obj.laning_phase
                    if position_obj.laning_phase
                    else 0
                )
                team_score.flex += position_obj.flex
                team_score.overall += position_obj.overall
    for player_name, position in team:
        team_score.players[position] = player_name
    return team_score


def calculate_balance_score(team_a_score, team_b_score):
    return (
        0.6 * abs(team_a_score.overall - team_b_score.overall)
        + 0.3 * abs(team_a_score.laning_phase - team_b_score.laning_phase)
        + 0.1 * abs(team_a_score.flex - team_b_score.flex)
    )


def create_balanced_teams(players):
    all_players = [p.name for p in players]
    team_combinations = list(combinations(all_players, 5))
    best_balance = float('inf')
    best_teams = None

    for team_a_combo in team_combinations:
        team_b_combo = set(all_players) - set(team_a_combo)
        team_a_permutations = generate_position_permutations(
            team_a_combo, players
        )
        team_b_permutations = generate_position_permutations(
            team_b_combo, players
        )

        for team_a_perm, team_b_perm in product(
            team_a_permutations, team_b_permutations
        ):
            fix_ok = True
            if DEBUG:
                print(team_a_perm + team_b_perm)
            for (name, position) in zip(FIXES.keys(), FIXES.values()):
                if (name, position) not in team_a_perm + team_b_perm:
                    fix_ok = False
            if not fix_ok:
                continue
            team_a_score = calculate_team_score(team_a_perm, players)
            team_b_score = calculate_team_score(team_b_perm, players)
            # print(team_a_score.players, team_b_score.players, end="\n\n")
            if not (team_a_score.is_valid() and team_b_score.is_valid()):
                continue

            # calculate balance score for this configuration
            balance_score = calculate_balance_score(team_a_score, team_b_score)
            if balance_score < best_balance:
                best_balance = balance_score
                best_teams = (team_a_score, team_b_score)
    return best_teams


def __main__():
    players = [p for p in USER_POOL if p.playing]
    # print('Players:', players)
    num_players = len(players)
    # print("User Pool:", players, end="\n\n")
    print('_________________5v5 Scrim Roster_________________')
    print('Number of players: ', num_players)
    print('Not Playing:', [p.name for p in USER_POOL if not p.playing])

    if num_players < 10:
        print('Not enough players to create a game')
    elif num_players > 10:
        print('Too many players to create a game')

    # find the most balanced teams
    most_balanced_teams = create_balanced_teams(players)
    if not most_balanced_teams:
        print('No balanced teams could be found.')
        return
    else:
        team_a_score, team_b_score = most_balanced_teams

    print('Roster:')
    print(
        f'Team A [Laning: {team_a_score.laning_phase} Champion Pool: {team_a_score.flex} Overall: {team_a_score.overall}]',
        team_a_score,
        end='\n\n',
    )
    print(
        f'Team B [Laning: {team_b_score.laning_phase} Champion Pool: {team_b_score.flex} Overall: {team_b_score.overall}]',
        team_b_score,
        end='\n\n',
    )

__main__()
