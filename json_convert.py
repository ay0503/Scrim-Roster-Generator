
from team import *
import json

def create_player(name, positions):
    player = Player(name)
    for position_data in positions:
        lane = position_data['lane']
        overall = position_data['overall']
        laning_phase = position_data.get('laning_phase')
        champ_pool = position_data.get('champ_pool', [])
        position = Position(lane, overall, champ_pool, laning_phase)
        player.add_position(position)
    return player

def convert_to_json(user_pool):
    players = []
    for player_name, player_data in user_pool.items():
        positions = []
        for position_str in player_data.split(', '):
            if 'Top' in position_str:
                positions.append({'lane': 'Top', 'overall': float(position_str.split('[')[1].split(']')[0]), 'laning_phase': float(position_str.split('[')[2].split(']')[0])})
            elif 'Jungle' in position_str:
                positions.append({'lane': 'Jungle', 'overall': float(position_str.split('[')[1].split(']')[0]), 'laning_phase': None})
            elif 'Mid' in position_str:
                positions.append({'lane': 'Mid', 'overall': float(position_str.split('[')[1].split(']')[0]), 'laning_phase': float(position_str.split('[')[2].split(']')[0])})
            elif 'ADC' in position_str:
                positions.append({'lane': 'ADC', 'overall': float(position_str.split('[')[1].split(']')[0]), 'laning_phase': float(position_str.split('[')[2].split(']')[0])})
            elif 'Support' in position_str:
                positions.append({'lane': 'Support', 'overall': float(position_str.split('[')[1].split(']')[0]), 'laning_phase': float(position_str.split('[')[2].split(']')[0])})
        player = create_player(player_name, positions)
        players.append(player)

    json_data = []
    for player in players:
        player_data = {
            'name': player.name,
            'positions': [
                {
                    'lane': position.lane,
                    'overall': position.overall,
                    'laning_phase': position.laning_phase,
                    'champ_pool': position.champ_pool
                }
                for position in player.positions
            ],
            'playing': player.playing
        }
        json_data.append(player_data)

    return json_data

json_data = convert_to_json(user_pool)

# Write the JSON data to a file
with open('user_pool.json', 'w') as file:
    json.dump(json_data, file, indent=4)