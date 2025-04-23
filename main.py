import pypokedex as pokedex
import random

pokemon_id = random.randint(1, 151)
random_pokemon = pokedex.get(dex=pokemon_id)
print(random_pokemon)