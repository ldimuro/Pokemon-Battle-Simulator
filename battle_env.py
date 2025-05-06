import random
import numpy
from pokemon import Pokemon
from moves import Move
import pandas as pd
import numpy as np
from pokemon_enums import Status
import moves_handler
from trainer import Trainer

class BattleEnv:
    def __init__(self, trainer1, trainer2):
        self.trainer1: Trainer = trainer1
        self.trainer2: Trainer = trainer2

        self.player_pokemon: Pokemon = self.trainer1.party[0]
        self.opp_pokemon: Pokemon = self.trainer2.party[0]

        print(f'{trainer1.name} threw out:')
        self.player_pokemon.print_data()
        print(f'{trainer2.name} threw out:')
        self.opp_pokemon.print_data()


    def simulate_battle(self):
        
        turn = 1
        while len(self.trainer1.party) > 0 and len(self.trainer2.party) > 0:
            if turn == 100:
                print('STALEMATE')
                break

            player_move: Move = self.player_pokemon.use_move()
            opp_move: Move = self.opp_pokemon.use_move()

            # TODO: SET UP PRIORITY

            if self.player_pokemon.speed >= self.opp_pokemon.speed:
                first_pokemon, first_move = self.player_pokemon, player_move
                second_pokemon, second_move = self.opp_pokemon, opp_move
            else:
                first_pokemon, first_move = self.opp_pokemon, opp_move
                second_pokemon, second_move = self.player_pokemon, player_move

            print(f'=============================|TURN {turn}|=============================')
            print(f'{first_pokemon.name.upper()} temp_effects:', first_pokemon.temp_effects)
            print(f'{second_pokemon.name.upper()} temp_effects:', second_pokemon.temp_effects)
            self.print_game_state()

            # CHECK TO SEE IF POKEON LOSES ITS TURN
            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = moves_handler.apply_status_effects(first_pokemon)

            if first_pokemon.is_fainted:
                if first_pokemon.owner == self.trainer1.name:
                    # Remove fainted pokemon from trainer and throw in next in line
                    self.trainer1.party.remove(first_pokemon)
                    self.player_pokemon = self.trainer1.party[0] if len(self.trainer1.party) > 0 else None
                    print(f'{self.trainer1.name} threw in:', end='')
                    self.player_pokemon.print_data() if self.player_pokemon is not None else ''
                    continue
                else:
                    # Remove fainted pokemon from trainer and throw in next in line
                    self.trainer2.party.remove(first_pokemon)
                    self.opp_pokemon = self.trainer2.party[0] if len(self.trainer2.party) > 0 else None
                    print(f'{self.trainer2.name} threw in:', end='')
                    self.opp_pokemon.print_data() if self.opp_pokemon is not None else ''
                    continue

            # One trainer has no pokemon left to play
            if self.player_pokemon is None or self.opp_pokemon is None:
                break


            # First Move
            if not has_lost_turn:
                self.execute_move(first_move, first_pokemon, second_pokemon)

            
            print(f'------------------------------------------------------------------')


            # CHECK TO SEE IF POKEMON LOSES ITS TURN
            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = moves_handler.apply_status_effects(second_pokemon)

            if second_pokemon.is_fainted:
                # Remove fainted pokemon from trainer and throw in next in line
                if second_pokemon.owner == self.trainer1.name:
                    self.trainer1.party.remove(second_pokemon)
                    self.player_pokemon = self.trainer1.party[0] if len(self.trainer1.party) > 0 else None
                    print(f'{self.trainer1.name} threw in:', end='')
                    self.player_pokemon.print_data() if self.player_pokemon is not None else ''
                    continue
                else:
                    # Remove fainted pokemon from trainer and throw in next in line
                    self.trainer2.party.remove(second_pokemon)
                    self.opp_pokemon = self.trainer2.party[0] if len(self.trainer2.party) > 0 else None
                    print(f'{self.trainer2.name} threw in:', end='')
                    self.opp_pokemon.print_data() if self.opp_pokemon is not None else ''
                    continue


            # One trainer has no pokemon left to play
            if self.player_pokemon is None or self.opp_pokemon is None:
                break


            self.print_game_state()

            
            # Second Move
            if not has_lost_turn:
                self.execute_move(second_move, second_pokemon, first_pokemon)

            turn += 1


            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            print(f'{self.trainer1.name}: {len(self.trainer1.party)}, {self.trainer2.name} pokemon: {len(self.trainer2.party)} ')


            

        if len(self.trainer1.party) > 0:
            winner = self.trainer1.name
            result = 1
        else:
            winner = self.trainer2.name
            result = 0

        print(f'\n{winner} HAS WON THE BATTLE {len(self.trainer1.party) if len(self.trainer1.party) > 0 else len(self.trainer2.party)}-0!')

        return result


    def execute_move(self, move: Move, attacker: Pokemon, defender: Pokemon):
        print(f'{attacker.name.upper()} uses {move.name.upper()}')

        hit_chance = moves_handler.get_hit_chance(move, attacker, defender)

        if hit_chance == 1 or random.random() <= hit_chance:
            moves_handler.handle_move_effects(move, attacker, defender)
        else:
            print(f'{attacker.name.upper()}\'s move missed')


    
    def print_game_state(self):
        status_icon = {
            Status.PARALYZED: '⚡️',
            Status.ASLEEP: '💤',
            Status.BURNED: '🔥',
            Status.POISONED: '☠️',
            Status.FROZEN: '❄️',
            'confused': '🌀',
            Status.NONE: '',
        }
        
        hp_ratio = self.player_pokemon.curr_hp / self.player_pokemon.base_hp
        filled = int(hp_ratio * 16)
        empty = 16 - filled
        name = self.player_pokemon.name.upper() + ' lvl' + str(self.player_pokemon.level)

        status = status_icon['confused'] if self.player_pokemon.is_confused else '' + status_icon[self.player_pokemon.status]

        print(f"{name:<20}\t[{'█' * filled}{'-' * empty}] {status} HP {self.player_pokemon.curr_hp}/{self.player_pokemon.base_hp}")

        hp_ratio = self.opp_pokemon.curr_hp / self.opp_pokemon.base_hp
        filled = int(hp_ratio * 16)
        empty = 16 - filled
        name = self.opp_pokemon.name.upper() + ' lvl' + str(self.opp_pokemon.level)

        status = status_icon['confused'] if self.opp_pokemon.is_confused else '' + status_icon[self.opp_pokemon.status]

        print(f"{name:<20}\t[{'█' * filled}{'-' * empty}] {status} HP {self.opp_pokemon.curr_hp}/{self.opp_pokemon.base_hp}")



    

    