import random
import numpy

class BattleEnv:
    def __init__(self, curr_pokemon, opp_pokemon):
        self.player_pokemon = curr_pokemon
        self.opp_pokemon = opp_pokemon

    