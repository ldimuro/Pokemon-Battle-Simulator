from pokemon import Pokemon
from battle_env import BattleEnv
import moves
import random
import numpy as np
import main_helper

main_helper.set_seed(random.randint(0, 1000000))

version = 'red-blue'

agent_pokemon = Pokemon(random.randint(1, 152), version) # 4 for charmander
agent_pokemon.print_data()

opp_pokemon = Pokemon(random.randint(1, 152), version) # 7 for squirtle
opp_pokemon.print_data()

env = BattleEnv(agent_pokemon, opp_pokemon)

env.start_battle()

