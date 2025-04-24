from pokemon import Pokemon
from battle_env import BattleEnv
import moves
import random
import numpy as np
import main_helper

# 881140 Caterpie vs Metapod
# 728127 instant Self-Destruct
# 679815 interesting battle Hitmonlee vs Chansey
seed = random.randint(0, 1000000)
main_helper.set_seed(seed)

version = 'red-blue'

agent_pokemon = Pokemon(random.randint(1, 151), version) # 4 for charmander
agent_pokemon.print_data()

opp_pokemon = Pokemon(random.randint(1, 151), version) # 7 for squirtle
opp_pokemon.print_data()

env = BattleEnv(agent_pokemon, opp_pokemon)

env.start_battle()

