from pokemon import Pokemon
from battle_env import BattleEnv
import moves as moves_db
import random

version = 'red-blue'

agent_pokemon = Pokemon(4, version)
agent_pokemon.print_data()

opp_pokemon = Pokemon(7, version) #random.randint(1, 151)
opp_pokemon.print_data()

moves = moves_db.get_moves_db()
print('moves:', moves)

env = BattleEnv(agent_pokemon, opp_pokemon)