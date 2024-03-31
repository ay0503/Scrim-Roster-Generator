from flask import Flask, render_template, request, jsonify
from itertools import combinations, product
from user_data import *

# TODO create calendar entries (google calendar API)

app = Flask(__name__)

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

user_pool['TSOHN'].playing = False
user_pool['dotoeri'].playing = True
user_pool['DK_Showmaker'].playing = True
user_pool['zxczxc'].playing = True
user_pool['Zinoo'].playing = True
user_pool['Eightine'].playing = False
user_pool['JustLikeHim'].playing = True
user_pool['VexOnTheBeach'].playing = True
user_pool['muteallgoodgame'].playing = False
user_pool['LukeyParkey'].playing = True
user_pool['jenyu62'].playing = True
user_pool['KoreanSante'].playing = True
user_pool['wonton'].playing = True
USER_POOL = list(user_pool.values())

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
    print(players)
    all_players = [p.name for p in players]
    best_balance = float('inf')
    best_teams = None
    alternatives = []
    for team_a in combinations(all_players, 5):
        team_b = set(all_players) - set(team_a)
        print(set(team_a), team_b)
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
            if len(players) < 10 or (
                team_a_score.is_valid() and team_b_score.is_valid()
            ):
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


@app.route('/')
def index():
    print('Starting ')
    return render_template('index.html')


positions = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
registered_players = [
    TBA('TBA' + str(i), positions[i % 5])
    for i in range(len((positions + positions)))
]
# registered_players = [p for p in user_pool.values() if p.playing]
# print(registered_players)

@app.route('/register', methods=['POST'])
def register_player():
    data = request.json
    player_name = data.get('name')

    if player_name not in [
        player.name for player in registered_players
    ]:  # Check if the name is not already in the list
        # Find the player object by name from USER_POOL
        player = next((p for p in USER_POOL if p.name == player_name), None)
        if player:
            for i in range(len(registered_players)):
                if (
                    player.positions[0].lane
                    == registered_players[i].positions[0].lane
                ):
                    registered_players[i] = player
                    break

    # Once 10 players have registered, generate the 5v5 matchup
    best_teams, alternatives = create_balanced_teams(registered_players)
    print(best_teams, alternatives)
    if len(registered_players) < 10 or best_teams:
        # Convert the best team matchup to a suitable format for the frontend
        matchup = convert_teams_to_matchup_format(best_teams)
        # Here, you may want to include alternative matchups or handle them differently
        print(
            jsonify(
                {
                    'players': [p.name for p in registered_players],
                    'matchup': matchup,
                }
            )
        )
        return jsonify(
            {
                'players': [p.name for p in registered_players],
                'matchup': matchup,
            }
        )

    return jsonify(
        {
            'players': [p.name for p in registered_players],
            'message': 'Waiting for more players.',
        }
    )


def convert_teams_to_matchup_format(teams):
    # Assuming teams is a tuple with each team being a list of tuples (player, position)
    team_blue, team_red = teams
    print(type(teams[0]), end='\n\n\n\n')
    return {
        'blue': {
            position.lower(): team_blue.players[position]
            if 'TBA' not in team_blue.players[position]
            else 'TBA'
            for position in team_blue.players
        },
        'red': {
            position.lower(): team_red.players[position]
            if 'TBA' not in team_red.players[position]
            else 'TBA'
            for position in team_red.players
        },
    }


if __name__ == '__main__':
    app.run(debug=True)
