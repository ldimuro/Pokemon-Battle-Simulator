from pokemon import Pokemon
import random

version = 'red-blue'

agent_pokemon = Pokemon(4, version)
agent_pokemon.print_data()

random_pokemon = Pokemon(random.randint(1, 151), version)
random_pokemon.print_data()