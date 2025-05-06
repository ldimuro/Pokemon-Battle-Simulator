import random
from pokemon import Pokemon
from main_helper import version_pokemon_range

class Trainer:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        
        # Randomly select pokemon of size party_size
        self.party_size = 3
        self.party = [Pokemon(random.randint(1, version_pokemon_range[self.version]), self.version) for i in range(self.party_size)]
        print(f'Trainer {self.name}, with Pokemon: [{[mon.name for mon in self.party]}]')