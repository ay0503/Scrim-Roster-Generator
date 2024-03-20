# TODO Late game potential
# TODO (jg, top), (adc, sup) synergy


class Player:

    def __init__(self, name) -> None:
        self.name = name
        self.positions = []
        self.playing = True

    def add_position(self, position):
        self.positions.append(position)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"\n\n{self.name}: Positions{self.positions}"

    def __eq__(self, other) -> bool:
        return self.name == other.name


class Position:

    def __init__(self, lane, overall, champ_pool, laning_phase=None) -> None:
        self.lane = lane
        self.champ_pool = champ_pool

        # Skill level
        self.laning_phase = laning_phase
        self.overall = overall

    def __repr__(self) -> str:
        return f"\n{self.lane}: Overall[{self.overall}] Laning[{self.laning_phase}]"


class Team:

    def __init__(self) -> None:
        self.laning_phase = 0
        self.overall = 0
        self.positions_filled = set()
        self.players = {
            "Top": None,
            "Jungle": None,
            "Mid": None,
            "ADC": None,
            "Support": None,
        }

    def __repr__(self) -> str:
        return f"""\n
              Top:     {self.players.get('Top', None)}\n
              Jungle:  {self.players.get('Jungle', None)}\n
              Mid:     {self.players.get('Mid', None)}\n
              ADC:     {self.players.get('ADC', None)}\n
              Support: {self.players.get("Support", None)}"""

    def is_valid(self):
        for position in self.players:
            if self.players[position] == None:
                return False
        return True


# Create player objects
user_pool = []
TSOHN = Player("TSOHN")
TSOHN.add_position(
    Position(
        "Top", laning_phase=6, overall=7, champ_pool=["Aatrox", "Jax", "Mordekaiser"]
    )
)

dotoeri = Player("dotoeri")
dotoeri.add_position(
    Position(
        "Jungle",
        overall=9.5,
        champ_pool=["Graves", "Lee-sin", "Taliyah", "Ekko", "Diana", "Lillia"],
    )
)
dotoeri.add_position(
    Position(
        "ADC",
        overall=5,
        laning_phase=7,
        champ_pool=["Ezreal", "Kaisa", "Samira", "Jhin", "Aphelios", "Sivir", "Vayne"],
    )
)

DK_Showmaker = Player("DK_Showmaker")
DK_Showmaker.add_position(
    Position(
        "Mid",
        laning_phase=8.5,
        overall=9,
        champ_pool=["Ahri", "Syndra", "Sylas", "Kassadin", "Yasuo", "Akali"],
    )
)
DK_Showmaker.add_position(
    Position(
        "Top",
        laning_phase=7,
        overall=7,
        champ_pool=["Aatrox", "Renekton", "Jayce", "Camille", "Gragas"],
    )
)

zxczxc = Player("zxczxc")
zxczxc.add_position(
    Position(
        "ADC",
        laning_phase=7,
        overall=7,
        champ_pool=["Senna", "Ezreal", "Vayne", "Xayah", "Lucian"],
    )
)
zxczxc.add_position(
    Position(
        "Mid",
        laning_phase=10,
        overall=9,
        champ_pool=[
            "Ahri",
            "Akali",
            "Hwei",
            "Cassiopeia",
            "Vladmir",
            "Orianna",
            "Lee-sin",
        ],
    )
)
zxczxc.add_position(
    Position(
        "Support",
        overall=8.5,
        laning_phase=10,
        champ_pool=["Senna", "Thresh", "Shaco", "Hwei"],
    )
)

Zinoo = Player("Zinoo")
Zinoo.add_position(
    Position(
        "ADC",
        laning_phase=9,
        overall=8.5,
        champ_pool=[
            "Jinx",
            "Zeri",
            "Vayne",
            "Varus",
            "Kaisa",
            "Xayah",
            "Caitlyn",
            "Samira",
            "Kalista",
        ],
    )
)

Eightine = Player("Eightine")
Eightine.add_position(
    Position(
        "Support",
        overall=8,
        laning_phase=8.5,
        champ_pool=[
            "Thresh",
            "Blitzcrank",
            "Rakan",
            "Leona",
            "Nautilus",
            "Alistar",
            "Morgana",
        ],
    )
)
Eightine.add_position(
    Position(
        "ADC",
        laning_phase=7,
        overall=7.5,
        champ_pool=["Nilah", "Aphelios", "Ezreal", "Kaisa", "Caitlyn", "Jinx"],
    )
)

JustLikeHim = Player("JustLikeHim")
JustLikeHim.add_position(
    Position("Jungle", overall=9.5, champ_pool=["Khazix", "Vi", "Xin-Zhao"])
)

VexOnTheBeach = Player("VexOnTheBeach")
VexOnTheBeach.add_position(
    Position(
        "Mid",
        laning_phase=7,
        overall=7.5,
        champ_pool=["Vex", "Lissandra", "Swain", "Ahri", "Neeko"],
    )
)

muteallgoodgame = Player("muteallgoodgame")
muteallgoodgame.add_position(
    Position(
        "ADC",
        laning_phase=9,
        overall=10,
        champ_pool=[
            "Ezreal",
            "Kaisa",
            "Smolder",
            "Lucian",
            "Caitlyn",
            "Samira",
            "Ashe",
        ],
    )
)

LukeyParkey = Player("LukeyParkey")
LukeyParkey.add_position(
    Position(
        "Support",
        overall=7.5,
        laning_phase=8.5,
        champ_pool=["Thresh", "Poppy", "Rakan", "Milio", "Alistar"],
    )
)
LukeyParkey.add_position(
    Position(
        "Top", laning_phase=8, overall=8, champ_pool=["Poppy", "Illaoi", "Shen", "Zac"]
    )
)

jenyu62 = Player("jenyu62")
jenyu62.add_position(
    Position(
        "Support",
        laning_phase=5,
        overall=6,
        champ_pool=["Rakan", "Leona", "Neeko", "Lux", "Senna"],
    )
)

KoreanSante = Player("KoreanSante")
KoreanSante.add_position(
    Position(
        "Top",
        overall=9,
        laning_phase=10,
        champ_pool=["KSante", "Volibear", "Aatrox", "Mordekaiser", "Pantheon", "Nasus"],
    )
)

wonton = Player("wonton")
wonton.add_position(
    Position(
        "Support",
        overall=8,
        laning_phase=9.5,
        champ_pool=["Thresh", "Rumble", "Blitzcrank", "Morgana", "Senna"],
    )
)
wonton.add_position(
    Position(
        "Jungle", overall=8, champ_pool=["Sejuani", "Lee-sin", "Kayn", "Gragas", "Ekko"]
    )
)
wonton.add_position(
    Position(
        "Mid",
        overall=7,
        laning_phase=6,
        champ_pool=["Viktor", "Orianna", "Zoe", "Syndra", "Galio", "Kassadin"],
    )
)  # TODO needs change

# Add all users
user_pool.append(TSOHN)
user_pool.append(dotoeri)
user_pool.append(DK_Showmaker)
user_pool.append(zxczxc)
user_pool.append(Zinoo)
user_pool.append(Eightine)
user_pool.append(JustLikeHim)
user_pool.append(VexOnTheBeach)
user_pool.append(muteallgoodgame)
user_pool.append(LukeyParkey)
user_pool.append(jenyu62)
user_pool.append(KoreanSante)
user_pool.append(wonton)
