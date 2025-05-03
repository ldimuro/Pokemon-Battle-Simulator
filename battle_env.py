import random
import numpy
from pokemon import Pokemon
from moves import Move
import pandas as pd
import numpy as np
from pokemon_enums import Status
import special_moves

class BattleEnv:
    def __init__(self, curr_pokemon: Pokemon, opp_pokemon: Pokemon):
        self.player_pokemon = curr_pokemon
        self.opp_pokemon = opp_pokemon

        # print(f'{self.player_pokemon.name.upper()} ({self.player_pokemon.curr_hp} HP) vs. {self.opp_pokemon.name.upper()} ({self.opp_pokemon.curr_hp} HP)')

    def start_battle(self):
        
        turn = 1
        while self.player_pokemon.curr_hp > 0 and self.opp_pokemon.curr_hp > 0:
            if turn == 100:
                print('STALEMATE')
                break

            player_move: Move = self.player_pokemon.use_move()
            opp_move: Move = self.opp_pokemon.use_move()

            if self.player_pokemon.speed >= self.opp_pokemon.speed:
                first_pokemon, first_move = self.player_pokemon, player_move
                second_pokemon, second_move = self.opp_pokemon, opp_move
            else:
                first_pokemon, first_move = self.opp_pokemon, opp_move
                second_pokemon, second_move = self.player_pokemon, player_move

            print(f'=============================|TURN {turn}|=============================')
            print('1st pokemon temp_effects:', first_pokemon.temp_effects)
            print('2nd pokemon temp_effects:', second_pokemon.temp_effects)
            self.print_game_state()

            # CHECK TO SEE IF POKEON LOSES ITS TURN
            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = self.apply_status_effects(first_pokemon)

            if first_pokemon.is_fainted:
                break

            # First Move
            if not has_lost_turn:
                self.execute_move(first_move, first_pokemon, second_pokemon)

            
            print(f'-----------------------------------------------------------------------')


            # CHECK TO SEE IF POKEMON LOSES ITS TURN
            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = self.apply_status_effects(second_pokemon)

            if second_pokemon.is_fainted:
                break

            self.print_game_state()

            # Second Move
            if not has_lost_turn:
                self.execute_move(second_move, second_pokemon, first_pokemon)

            turn += 1
            
        self.print_game_state()

        winner = self.player_pokemon if self.player_pokemon.curr_hp > 0 else self.opp_pokemon
        print(f'{winner.name.upper()} HAS WON THE BATTLE!')




    def execute_move(self, move: Move, attacker: Pokemon, defender: Pokemon):
        print(f'{attacker.name.upper()} uses {move.name.upper()}')

        hit_chance = self.get_hit_chance(move, attacker, defender)*100
        if hit_chance == 1 or random.randint(0, 100) <= hit_chance:
            special_moves.handle_move_effects(move, attacker, defender)
        else:
            print(f'{attacker.name.upper()}\'s move missed')



    def apply_status_effects(self, pokemon: Pokemon):
        lose_turn = False

        # Handle confusion functionality
        if pokemon.is_confused:
            pokemon.confused_count += 1
            if pokemon.curr_confused_count == pokemon.confused_count:
                pokemon.remove_confused()
            else:
                print(f'{pokemon.name.upper()} is confused')
                if random.random() <= 0.5:
                    print(f'{pokemon.name.upper()} hurt itself in it\'s confusion')
                    confusion_damage_move = Move(
                        name='confusion-damage',
                        type='*',
                        power=40,
                        accuracy=100,
                        category='physical',
                        pp=25,
                        effect='confusion damage'
                    )
                    confusion_damage = special_moves.calculate_damage(confusion_damage_move, pokemon, pokemon)
                    pokemon.reduce_hp(confusion_damage)
                    lose_turn = True

        # Handle all other status conditions
        match pokemon.status:
            case Status.PARALYZED:
                print(f'{pokemon.name.upper()} is paralyzed')
                pokemon.speed *= 0.25
                if random.random() < 0.25:
                    lose_turn = True
                    print(f'{pokemon.name.upper()} is paralyzed. It can\'t move!')
            case Status.ASLEEP:
                # print(f'curr status_count: {pokemon.curr_status_count}, status_count: {pokemon.status_count}')
                if pokemon.curr_status_count == pokemon.status_count:
                    pokemon.remove_status()
                    print(f'{pokemon.name.upper()} woke up!')
                else:
                    pokemon.curr_status_count += 1
                    lose_turn = True
                    print(f'{pokemon.name.upper()} is asleep')
            case Status.POISONED:
                pokemon.reduce_hp(pokemon.base_hp/16)
                print(f'{pokemon.name.upper()} was hurt by poison ({np.round(pokemon.base_hp/16, 2)} Damage)')
            case Status.BURNED:
                pokemon.attack *= 0.5
                pokemon.reduce_hp(pokemon.base_hp/16)
                print(f'{pokemon.name.upper()} was hurt by its burn')
            case Status.FROZEN:
                lose_turn = True
                print(f'{pokemon.name.upper()} is frozen. It can\'t move!')
            case _:
                pass
            
        return lose_turn

    def get_hit_chance(self, move: Move, attacker: Pokemon, defender: Pokemon):
        accuracy_stage_multipliers = {
            -6: 0.33, -5: 0.375, -4: 0.43, -3: 0.5, -2: 0.6, -1: 0.75,
             0: 1.0,  1: 1.33,   2: 1.66,  3: 2.0,  4: 2.33,  5: 2.66, 6: 3.0
        }

        accuracy = accuracy_stage_multipliers[attacker.accuracy_tier]
        evasiveness= accuracy_stage_multipliers[defender.evasiveness_tier]
        base = 100 if move.accuracy == -1 else move.accuracy / 100.0
        return base * (accuracy / evasiveness)

    
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



    

    