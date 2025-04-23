import pypokedex as pokedex
from moves import moves_db
import random

class Pokemon:
    def __init__(self, pokemon_id, version):
        pokemon = pokedex.get(dex=pokemon_id)
        print('pokemon:', pokemon)

        self.id = pokemon.dex
        self.name = pokemon.name
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.types = pokemon.types
        self.abilities = [ability.name for ability in pokemon.abilities]

        base_stats = pokemon.base_stats
        self.hp = base_stats.hp
        self.attack = base_stats.attack
        self.defense = base_stats.defense
        self.sp_atk = base_stats.sp_atk
        self.sp_def = base_stats.sp_def
        self.speed = base_stats.speed

        self.atk_tier = 0
        self.def_tier = 0
        self.sp_atk_tier = 0
        self.sp_def_tier = 0
        self.speed_tier = 0
        self.evasiveness_tier = 0

        all_moves = [move.name for move in pokemon.moves[version]]
        self.moves = self.choose_moves(all_moves)

        self.sprites = pokemon.sprites
        self.other_sprites = pokemon.other_sprites
        self.version_sprites = pokemon.version_sprites

    # Choose 4 moves from all of Pokemon's learnable moves
    def choose_moves(self, moves):
        final_moves = []

        formatted_moves = [moves_db[move] for move in moves]

        if len(formatted_moves) > 4:
            # At least 1 move must be do damage
            damage_moves = [move for move in formatted_moves if move.category == 'physical'] + [move for move in formatted_moves if move.category == 'special']
            random_damage_move = random.choice(damage_moves)
            final_moves.append(random_damage_move)
            formatted_moves.remove(random_damage_move)

            # At least 1 move must be of the same type as the Pokemon
            same_type_moves = [move for move in formatted_moves if move.move_type in self.types]
            random_same_type_move = random.choice(same_type_moves)
            final_moves.append(random_same_type_move)
            formatted_moves.remove(random_same_type_move)

            move3 = random.choice(formatted_moves)
            final_moves.append(move3)
            formatted_moves.remove(move3)

            move4 = random.choice(formatted_moves)
            final_moves.append(move4)
            formatted_moves.remove(move4)
        else:
            final_moves = formatted_moves

        return final_moves

        

    def print_data(self):
        print('===============================================================================')
        print(f'Name: {self.name}')
        print(f'Types: {' '.join(self.types)}')
        print(f'Stats: HP:{self.hp} | ATK:{self.attack} | DEF:{self.defense} | SP ATK:{self.sp_atk} | SP DEF:{self.sp_def} | SPEED:{self.speed}')
        print(f'Moves: ', end='')
        for move in self.moves:
            print(f'{move.name} ', end='')
        print()
        print(f'Abilities: {' '.join(self.abilities)}')
        print('===============================================================================')