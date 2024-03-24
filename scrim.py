from itertools import combinations, product
from user_data import *

DEBUG = False
USER_POOL = list(user_pool.values())
FIXES = {
    'DK_Showmaker': 'Mid',
    # 'LukeyParkey': 'Top',
    # 'dotoeri': 'Jungle',
    # 'Eightine': 'Support',
    'wonton': 'Support',
    'LukeyParkey': 'Top',
    # 'Eightine': 'ADC',
}
SYNERGIES = [
    {'muteallgoodgame': 'ADC', 'zxczxc': 'Support'},
    {'JustLikeHim': 'Jungle', 'KoreanSante': 'Top'},
]


def generate_position_permutations(team, players):
    return list(
        product(
            *[
                [(player.name, position.lane) for position in player.positions]
                for player in players
                if player.name in team
            ]
        )
    )


def calculate_team_score(team, players):
    team_score = Team()
    for player_name, position in team:
        player = next((p for p in players if p.name == player_name), None)
        if player:
            position_obj = next(
                (pos for pos in player.positions if pos.lane == position), None
            )
            if position_obj:
                team_score.laning_phase += position_obj.laning_phase or 0
                team_score.flex += position_obj.flex
                team_score.overall += position_obj.overall
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
    best_balance = float('inf')
    best_teams = None
    alternatives = []
    for team_a in combinations(all_players, 5):
        team_b = set(all_players) - set(team_a)
        for team_a_perm, team_b_perm in product(
            generate_position_permutations(team_a, players),
            generate_position_permutations(team_b, players),
        ):
            if not all(
                (name, position) in team_a_perm + team_b_perm
                for name, position in FIXES.items()
            ):
                continue
            team_a_score, team_b_score = calculate_team_score(
                team_a_perm, players
            ), calculate_team_score(team_b_perm, players)
            if team_a_score.is_valid() and team_b_score.is_valid():
                balance_score = calculate_balance_score(
                    team_a_score, team_b_score
                )
                if balance_score < best_balance:
                    best_balance = balance_score
                    alternatives.append(best_teams) if best_teams else None
                    best_teams = (team_a_score, team_b_score)
    return best_teams, alternatives[-2:]


def print_teams(team_scores):
    team_a_score, team_b_score = team_scores
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


def __main__():
    players = [p for p in USER_POOL if p.playing]
    num_players = len(players)
    print('_________________5v5 Scrim Roster_________________')
    print('Number of players:', num_players)
    print('Not Playing:', [p.name for p in USER_POOL if not p.playing])

    if num_players < 10:
        print('Not enough players to create a game')
    elif num_players > 10:
        print('Too many players to create a game')
    else:
        most_balanced_teams, alternatives = create_balanced_teams(players)
        if most_balanced_teams:
            print('Roster:')
            print_teams(most_balanced_teams)
            print('Alternatives:')
            for team_scores in alternatives:
                print_teams(team_scores)
        else:
            print('No balanced teams could be found.')


__main__()
