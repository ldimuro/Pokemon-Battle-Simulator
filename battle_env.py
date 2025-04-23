import random
import numpy
from pokemon import Pokemon

class BattleEnv:
    def __init__(self, curr_pokemon: Pokemon, opp_pokemon: Pokemon):
        self.player_pokemon = curr_pokemon
        self.opp_pokemon = opp_pokemon

        print(f'{self.player_pokemon.name.upper()} vs. {self.opp_pokemon.name.upper()}')

    

    