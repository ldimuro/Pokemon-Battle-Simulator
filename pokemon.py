import pypokedex as pokedex

class Pokemon:
    def __init__(self, pokemon_id, version):
        pokemon = pokedex.get(dex=pokemon_id)

        self.id = pokemon.dex
        self.name = pokemon.name
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.types = pokemon.types
        self.abilities = pokemon.abilities

        base_stats = pokemon.base_stats
        self.hp = base_stats.hp
        self.attack = base_stats.attack
        self.defense = base_stats.defense
        self.sp_atk = base_stats.sp_atk
        self.sp_def = base_stats.sp_def
        self.speed = base_stats.speed

        all_moves = [move.name for move in pokemon.moves[version]]
        self.moves = self.choose_moves(all_moves)

        self.sprites = pokemon.sprites
        self.other_sprites = pokemon.other_sprites
        self.version_sprites = pokemon.version_sprites

    # Choose 4 moves from all of Pokemon's learnable moves
    # At least 1 move must be of the same type as the Pokemon
    # At least 1 move must be do damage
    def choose_moves(self, moves):
        pass

    def print_data(self):
        print('===============================================================================')
        print(f'Name: {self.name}')
        print(f'Types: {' '.join(self.types)}')
        print(f'Stats: HP:{self.hp} | ATK:{self.attack} | DEF:{self.defense} | SP ATK:{self.sp_atk} | SP DEF:{self.sp_def} | SPEED:{self.speed}')
        print(f'Moves: {self.moves}')
        print(f'Abilities: {self.abilities}')
        print('===============================================================================')