import pypokedex as pokedex
from moves import moves_db
import random
import requests
from PIL import Image
from io import BytesIO
from pokemon_enums import Status
import numpy as np

class Pokemon:
    def __init__(self, pokemon_id, version):
        pokemon = pokedex.get(dex=pokemon_id)

        self.id = pokemon.dex
        self.name = pokemon.name
        self.level = 50
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.types = pokemon.types
        self.abilities = [ability.name for ability in pokemon.abilities]

        # STATS
        base_stats = pokemon.base_stats
        self.hp = base_stats.hp
        self.attack = base_stats.attack
        self.defense = base_stats.defense
        self.sp_atk = base_stats.sp_atk
        self.sp_def = base_stats.sp_def
        self.speed = base_stats.speed
        self.overall_stats = self.hp + self.attack + self.defense + self.sp_atk + self.sp_def + self.speed
        self.is_fainted = False

        # BATTLE STATE
        self.curr_hp = self.hp
        self.status_condition = Status.NONE
        self.atk_tier = 0
        self.def_tier = 0
        self.sp_atk_tier = 0
        self.sp_def_tier = 0
        self.speed_tier = 0
        self.evasiveness_tier = 0
        self.crit_ratio = 1

        # MOVES
        all_moves = [move.name for move in pokemon.moves[version]]
        self.moves = self.choose_moves(all_moves)

        # SPRITES
        self.sprites = pokemon.sprites
        self.other_sprites = pokemon.other_sprites
        self.version_sprites = pokemon.version_sprites

    def choose_moves(self, moves):
        final_moves = []

        # Retrieve move data from moves_db
        formatted_moves = [moves_db[move] for move in moves]

        # If Pokemon is able to learn 5+ total moves, randomly select 4 of them
        if len(formatted_moves) > 4:
            # At least 1 move must be do damage
            damage_moves = [move for move in formatted_moves if move.category == 'physical'] + [move for move in formatted_moves if move.category == 'special']
            random_damage_move = random.choice(damage_moves)
            final_moves.append(random_damage_move)
            formatted_moves.remove(random_damage_move)

            # At least 1 move must be of the same type as the Pokemon (if there are any)
            same_type_moves = [move for move in formatted_moves if move.type in self.types]
            if len(same_type_moves) > 0:
                random_same_type_move = random.choice(same_type_moves)
            else:
                random_same_type_move = random.choice(formatted_moves)
            final_moves.append(random_same_type_move)
            formatted_moves.remove(random_same_type_move)

            # Random Move #3
            move3 = random.choice(formatted_moves)
            final_moves.append(move3)
            formatted_moves.remove(move3)

            # Random Move #4
            move4 = random.choice(formatted_moves)
            final_moves.append(move4)
            formatted_moves.remove(move4)
        else:
            final_moves = formatted_moves

        return final_moves
    
    def use_move(self):
        return random.choice(self.moves)
    
    def reduce_hp(self, damage):
        self.curr_hp = max(0, np.round(self.curr_hp - damage, 2))
        if self.curr_hp <= 0:
            self.is_fainted = True
            print(f'{self.name.upper()} fainted!')

        

    def print_data(self):
        print('===============================================================================')
        print(f'Name: {self.name.upper()}')
        print(f'Types: {' '.join(self.types)}')
        print(f'Stats: HP:{self.hp} | ATK:{self.attack} | DEF:{self.defense} | SP ATK:{self.sp_atk} | SP DEF:{self.sp_def} | SPEED:{self.speed} | [OVR: {self.overall_stats}]')
        print(f'Moves: ', end='')
        for move in self.moves:
            print(f'{move.name.upper()} ', end='')
        print()
        print(f'Abilities: {' '.join(self.abilities)}')
        print('===============================================================================')

    def show_sprite(self):
        sprite_url = self.sprites[0]['default']
        if sprite_url:
            response = requests.get(sprite_url)
            img = Image.open(BytesIO(response.content))
            img.show()
        else:
            print('No sprite found.')