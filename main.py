from pokemon import Pokemon
from battle_env import BattleEnv
import moves
import random

version = 'red-blue'

agent_pokemon = Pokemon(random.randint(1, 151), version) # 4 for charmander
agent_pokemon.print_data()

opp_pokemon = Pokemon(random.randint(1, 151), version) # 7 for squirtle
opp_pokemon.print_data()

env = BattleEnv(agent_pokemon, opp_pokemon)