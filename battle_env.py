import random
import numpy
from pokemon import Pokemon
from moves import Move
import pandas as pd
import numpy as np

class BattleEnv:
    def __init__(self, curr_pokemon: Pokemon, opp_pokemon: Pokemon):
        self.player_pokemon = curr_pokemon
        self.opp_pokemon = opp_pokemon

        # print(f'{self.player_pokemon.name.upper()} ({self.player_pokemon.curr_hp} HP) vs. {self.opp_pokemon.name.upper()} ({self.opp_pokemon.curr_hp} HP)')

    def start_battle(self):
        
        turn = 1
        while self.player_pokemon.curr_hp > 0 and self.opp_pokemon.curr_hp > 0:

            player_move: Move = self.player_pokemon.use_move()
            opp_move: Move = self.opp_pokemon.use_move()

            if self.player_pokemon.speed >= self.opp_pokemon.speed:
                first_pokemon, first_move = self.player_pokemon, player_move
                second_pokemon, second_move = self.opp_pokemon, opp_move
            else:
                first_pokemon, first_move = self.opp_pokemon, opp_move
                second_pokemon, second_move = self.player_pokemon, player_move

            print(f'=-=-=-=-=-=-=-=|TURN {turn}|=-=-=-=-=-=-=-=')
            self.print_game_state()

            # First Move
            move_result = self.execute_move(first_move, first_pokemon, second_pokemon)
            turn += 1

            # Second Move
            if not second_pokemon.is_fainted:
                # print(f'=-=-=-=-=-=-=-=|TURN {turn}|=-=-=-=-=-=-=-=')
                # self.print_game_state()
                self.execute_move(second_move, second_pokemon, first_pokemon)
                # turn += 1
            

        winner = self.player_pokemon if self.player_pokemon.curr_hp > 0 else self.opp_pokemon
        print(f'{winner.name.upper()} HAS WON THE BATTLE!')




    def execute_move(self, move: Move, attacker: Pokemon, defender: Pokemon):
        print(f'{attacker.name.upper()} uses {move.name.upper()} on {defender.name.upper()}')

        match move.category:
            case ('physical' | 'special'):
                damage = self.calculate_damage(move, attacker, defender)
                defender.reduce_hp(damage)
            case 'status':
                pass
            case _:
                pass

        return f'{attacker.name.upper()} uses {move.name.upper()} on {defender.name.upper()}'

    def calculate_damage(self, move: Move, attacker: Pokemon, defender: Pokemon):
        type_effectivenss_chart = pd.read_csv('type_effectiveness.csv', index_col=0)
        a = attacker.sp_atk if move.category == 'special' else attacker.attack
        d = defender.sp_def if move.category == 'special' else defender.defense
        stab = 1.5 if move.type in attacker.types else 1
        type1 = type_effectivenss_chart.loc[move.type, defender.types[0]]
        type2 = 1 if len(defender.types) == 1 else type_effectivenss_chart.loc[move.type, defender.types[1]]
        type_effect = type1*type2
        random_val = random.randint(217, 255) / 255

        level_factor = (((2*attacker.level*attacker.crit_ratio)/5)+2)
        base = ((level_factor * move.power * (a / d)) / 50) + 2

        damage = np.round(base * stab * type_effect * random_val, 2)
        print('\tDAMAGE: ', damage)

        if type_effect == 2.0:
            print('\tIt\'s super effective!')
        elif type_effect == 0.5:
            print('\tIt\'s not very effective')
        elif type_effect == 0:
            print('\tIt has on effect')

        return damage
    
    def print_game_state(self):
        hp_ratio = self.player_pokemon.curr_hp / self.player_pokemon.hp
        filled = int(hp_ratio * 15)
        empty = 15 - filled
        print(f"{self.player_pokemon.name.upper()}\t[{'#' * filled}{'-' * empty}] HP {self.player_pokemon.curr_hp}/{self.player_pokemon.hp}")

        hp_ratio = self.opp_pokemon.curr_hp / self.opp_pokemon.hp
        filled = int(hp_ratio * 15)
        empty = 15 - filled
        print(f"{self.opp_pokemon.name.upper()}\t[{'#' * filled}{'-' * empty}] HP {self.opp_pokemon.curr_hp}/{self.opp_pokemon.hp}")



    

    