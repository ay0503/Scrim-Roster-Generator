class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.positions = []
        self.playing = True

    def add_position(self, position) -> None:
        self.positions.append(position)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f'\n\n{self.name}: Positions{self.positions}'

    def __eq__(self, other) -> bool:
        if type(other) == str:
            return other == self.name
        return self.name == other.name


class TBA(Player):
    def __init__(self, name, position) -> None:
        self.name = name
        self.positions = [Position(position, 0, [], 0)]
        self.playing = False

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f'\n\n{self.name}: Positions{self.positions}'

    def __eq__(self, other) -> bool:
        if type(other) == str:
            return other in self.name
        return self.name == other.name


class Position:
    def __init__(self, lane, overall, champ_pool, laning_phase=None) -> None:
        self.lane = lane
        self.champ_pool = champ_pool

        # Skill level
        self.laning_phase = laning_phase
        self.overall = overall
        self.flex = len(self.champ_pool)

    def __repr__(self) -> str:
        return f'\n{self.lane}: Overall[{self.overall}] Laning[{self.laning_phase}]'


class Team:
    def __init__(self) -> None:
        self.laning_phase = 0
        self.overall = 0
        self.flex = 0
        self.positions_filled = set()
        self.players = {
            'Top': None,
            'Jungle': None,
            'Mid': None,
            'ADC': None,
            'Support': None,
        }

    def __repr__(self) -> str:
        return f"""
    Top:     {self.players['Top']}
    Jungle:  {self.players['Jungle']}
    Mid:     {self.players['Mid']}
    ADC:     {self.players['ADC']}
    Support: {self.players['Support']}"""

    def is_valid(self) -> bool:
        for position in self.players:
            if self.players[position] == None:
                return False
        return True
