import pypokedex as pokedex
from moves import moves_db
import random
import requests
from PIL import Image
from io import BytesIO
from pokemon_enums import Status
import numpy as np

class Pokemon:
    def __init__(self, pokemon_id, owner, version):
        pokemon = pokedex.get(dex=pokemon_id)

        self.id = pokemon.dex
        self.name = pokemon.name
        self.owner = owner
        self.level = random.randint(25, 50)#50
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.types = pokemon.types
        self.abilities = [ability.name for ability in pokemon.abilities]

        # STATS
        base_stats = pokemon.base_stats
        self.base_hp = base_stats.hp
        self.base_attack = base_stats.attack
        self.base_defense = base_stats.defense
        self.base_sp_atk = base_stats.sp_atk
        self.base_sp_def = base_stats.sp_def
        self.base_speed = base_stats.speed
        self.overall_stats = self.base_hp + self.base_attack + self.base_defense + self.base_sp_atk + self.base_sp_def + self.base_speed
        
        self.is_fainted = False

        self.is_confused = False
        self.confused_count = 0
        self.curr_confused_count = 0

        self.status_count = 0
        self.curr_status_count = 1

        self.temp_effects = {}

        # BATTLE STATE
        self.curr_hp = self.base_hp
        self.status = Status.NONE
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.sp_atk = self.base_sp_atk
        self.sp_def = self.base_sp_def
        self.speed = self.base_speed
        self.atk_tier = 0
        self.def_tier = 0
        self.sp_atk_tier = 0
        self.sp_def_tier = 0
        self.speed_tier = 0
        self.evasiveness_tier = 0
        self.accuracy_tier = 0
        self.crit_ratio = 1

        # MOVES
        all_moves = [move.name for move in pokemon.moves[version]]
        self.moves = self.choose_moves(all_moves)

        self.move_history = []
        self.damage_history = []

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
        chosen_move = random.choice(self.moves)
        return chosen_move
    
    def update_move_history(self, move):
        self.move_history.append(move)
    
    def reduce_hp(self, damage):
        self.curr_hp = max(0, np.round(self.curr_hp - damage, 2))
        self.damage_history.append(damage)
        if self.curr_hp <= 0:
            self.is_fainted = True
            print(f'{self.name.upper()} fainted!')

    def recover_hp(self, recovered_hp):
        self.curr_hp = min(self.base_hp, np.round(self.curr_hp + recovered_hp, 2))
        print(f'{self.name.upper()} recovered {np.round(recovered_hp, 2)} HP')

    def add_status(self, status, status_count=0):
        if self.status == Status.NONE:
            self.status = status
            self.status_count = status_count
            print(f'{self.name.upper()} has become {self.status.value}!')
        else:
            print(f'{self.name.upper()} is already {self.status.value}')

    def remove_status(self):
        self.status = Status.NONE
        self.status_count = 0
        self.curr_status_count = 0

    def add_confused(self, status_count):
        if not self.is_confused:
            self.is_confused = True
            self.confused_count = status_count
            print(f'{self.name.upper()} became confusion!')
        else:
            print(f'{self.name.upper()} is already confused!')

    def remove_confused(self):
        self.is_confused = False
        self.confused_count = 0
        self.curr_confused_count = 0
        print(f'{self.name.upper()} snapped out of confusion!')

    def modifiy_stats_stage(self, stat, change):
        match stat:
            case 'attack':
                self.atk_tier += change
                self.atk_tier = max(-6, self.atk_tier) if self.atk_tier < 0 else min(6, self.atk_tier)
                self.attack = np.round(self.base_attack * self.stats_multiplier(self.atk_tier), 2)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.attack}')
            case 'defense':
                self.def_tier += change
                self.def_tier = max(-6, self.def_tier) if self.def_tier < 0 else min(6, self.def_tier)
                self.defense = np.round(self.base_defense * self.stats_multiplier(self.def_tier), 2)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.defense}')
            case 'sp_atk':
                self.sp_atk_tier += change
                self.sp_atk_tier = max(-6, self.sp_atk_tier) if self.sp_atk_tier < 0 else min(6, self.sp_atk_tier)
                self.sp_atk = np.round(self.base_sp_atk * self.stats_multiplier(self.sp_atk_tier), 2)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.sp_atk}')
            case 'sp_def':
                self.sp_def_tier += change
                self.sp_def_tier = max(-6, self.sp_def_tier) if self.sp_def_tier < 0 else min(6, self.sp_def_tier)
                self.sp_def = np.round(self.base_sp_def * self.stats_multiplier(self.sp_def_tier), 2)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.sp_def}')
            case 'speed':
                self.speed_tier += change
                self.speed_tier = max(-6, self.speed_tier) if self.speed_tier < 0 else min(6, self.speed_tier)
                self.speed = np.round(self.base_speed * self.stats_multiplier(self.speed_tier), 2)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.speed}')
            case 'evasiveness':
                self.evasiveness_tier += change
                self.evasiveness_tier = max(-6, self.evasiveness_tier) if self.evasiveness_tier < 0 else min(6, self.evasiveness_tier)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.evasiveness_tier}')
            case 'accuracy':
                self.accuracy_tier += change
                self.accuracy_tier = max(-6, self.accuracy_tier) if self.accuracy_tier < 0 else min(6, self.accuracy_tier)
                print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'} to {self.accuracy_tier}')
            case _:
                pass

        # print(f'{self.name.upper()}\'s {stat} {'increased' if change > 0 else 'decreased'}')

    def reset_stat(self, stat):
        match stat:
            case 'attack':
                self.atk_tier = 0
                self.attack = self.base_attack
            case 'defense':
                self.def_tier = 0
                self.defense = self.base_defense
            case 'sp_atk':
                self.sp_atk_tier = 0
                self.sp_atk = self.base_sp_atk
            case 'sp_def':
                self.sp_def_tier = 0
                self.sp_def = self.base_sp_def
            case 'speed':
                self.speed_tier = 0
                self.speed = self.base_speed
            case 'evasiveness':
                self.evasiveness_tier = 0
            case 'accuracy':
                self.accuracy_tier = 0


    def stats_multiplier(self, stage):
        stage_multipliers = { 
            6: 4.0, 5: 3.5, 4: 3.0, 3: 2.5, 2: 2.0, 1: 1.5, 0: 1.0, 
            -1: 0.67, -2: 0.5, -3: 0.4, -4: 0.33, -5: 0.29, -6: 0.25
        }
        
        return stage_multipliers[stage]


    def print_data(self):
        type_icon = {
            'normal': '⚪️',
            'fire': '🔥',
            'water': '💧',
            'electric': '⚡️',
            'grass': '🌿',
            'ice': '❄️',
            'fighting': '👊',
            'poison': '☠️',
            'ground': '🟤',
            'flying': '🪽',
            'psychic': '👁️',
            'bug': '🐞',
            'rock': '🪨',
            'ghost': '👻',
            'dragon': '🐲',
            'dark': '⚫️',
            'steel': '🩶',
            'fairy': '🦄'
        }

        # print('===============================================================================')
        print(f'{self.name.upper()}', end='')
        for type in self.types:
            print(f'{type_icon[type]} ', end='')
        print(' [', end='')
        for move in self.moves:
            print(f'{move.name.upper()} ', end='')
        print(f'] [HP:{self.base_hp} | ATK:{self.attack} | DEF:{self.defense} | SP ATK:{self.sp_atk} | SP DEF:{self.sp_def} | SPEED:{self.speed} | [OVR: {self.overall_stats}]]')
        # print('===============================================================================')

    def show_sprite(self):
        sprite_url = self.sprites[0]['default']
        if sprite_url:
            response = requests.get(sprite_url)
            img = Image.open(BytesIO(response.content))
            img.show()
        else:
            print('No sprite found.')