# TODO Late game potential
# TODO (jg, top), (adc, sup) synergy

import re
from team import *


def parse_skills(skills_text):
    players_skills = []
    current_position = None
    for line in skills_text.splitlines():
        if line.strip() and 'Players' in line:
            # This is a position heading
            current_position = line.split(' ')[
                0
            ]  # Assuming format "Position Players"
        elif current_position and ',' in line:
            # This is a player line under a position
            name, rest = line.split(',', 1)
            laning_phase = re.search(r'L: ([\d.]+)', rest)
            overall = re.search(r'O: ([\d.]+)', rest)
            players_skills.append(
                (
                    name.strip(),
                    current_position,
                    float(laning_phase.group(1)) if laning_phase else None,
                    float(overall.group(1)) if overall else None,
                )
            )
    return players_skills


def parse_champ_pools(champ_pools_text):
    pattern = re.compile(r'(\w+) Champ Pool: ([\w, ]+)')
    return {
        match.group(1): match.group(2).split(', ')
        for match in pattern.finditer(champ_pools_text)
    }


def create_players(skills, champ_pools):
    players = {}
    for name, position, laning, overall in skills:
        if name not in players:
            players[name] = Player(name)
        champ_pool = champ_pools.get(name, [])
        players[name].add_position(
            Position(position, overall, champ_pool, laning)
        )
    return players


skills_path = 'player_data/player_skills_by_position.txt'
champ_pool_path = 'player_data/player_champion_pools.txt'

skills_text = open(skills_path).read().strip()
champ_pools_text = open(champ_pool_path).read().strip()

skills = parse_skills(skills_text)
champ_pools = parse_champ_pools(champ_pools_text)
user_pool = create_players(skills, champ_pools)

# set participating players
user_pool['TSOHN'].playing = False
user_pool['dotoeri'].playing = True
user_pool['DK_Showmaker'].playing = True
user_pool['zxczxc'].playing = True
user_pool['Zinoo'].playing = False
user_pool['Eightine'].playing = True
user_pool['JustLikeHim'].playing = True
user_pool['VexOnTheBeach'].playing = True
user_pool['muteallgoodgame'].playing = True
user_pool['LukeyParkey'].playing = True
user_pool['jenyu62'].playing = False
user_pool['KoreanSante'].playing = True
user_pool['wonton'].playing = True

# print(user_pool.values())
