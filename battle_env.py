import random
import numpy
from pokemon import Pokemon
from moves import Move
import pandas as pd
import numpy as np
from pokemon_enums import Status

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

            print(f'=-=-=-=-=-=-=-=|TURN {turn}|=-=-=-=-=-=-=-=')
            self.print_game_state()

            # CHECK TO SEE IF POKEON LOSES ITS TURN

            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = self.apply_status_effects(first_pokemon)

            # First Move
            if not has_lost_turn:
                self.execute_move(first_move, first_pokemon, second_pokemon)

            if second_pokemon.is_fainted:
                break

            # CHECK TO SEE IF POKEON LOSES ITS TURN

            # APPLY STATUS (IF APPLICABLE)
            has_lost_turn = self.apply_status_effects(second_pokemon)

            # Second Move
            if not has_lost_turn:
                self.execute_move(second_move, second_pokemon, first_pokemon)

            turn += 1
            

        winner = self.player_pokemon if self.player_pokemon.curr_hp > 0 else self.opp_pokemon
        print(f'{winner.name.upper()} HAS WON THE BATTLE!')




    def execute_move(self, move: Move, attacker: Pokemon, defender: Pokemon):
        print(f'{attacker.name.upper()} uses {move.name.upper()}')

        hit_chance = self.get_hit_chance(move, attacker, defender)*100
        if hit_chance == 1 or random.randint(0, 100) <= hit_chance:
            match move.category:
                case ('physical' | 'special'):

                    if move.power == -1:
                        print('\tHANDLE ATTACKS WITH NO POWER')
                        
                        if move.name == 'seismic-toss':
                            damage = self.calculate_damage(move, attacker, defender, damage_override=attacker.level)
                            defender.reduce_hp(damage)
                        else:
                            damage = self.calculate_damage(move, attacker, defender, damage_override=0)
                            defender.reduce_hp(damage)
                    else:
                        damage = self.calculate_damage(move, attacker, defender)
                        defender.reduce_hp(damage)

                    if not defender.is_fainted:
                        if 'may' in move.effect:
                            print('\tHANDLE MAY CASES')
                        
                        if 'recover' in move.effect:
                            if 'inflicted' in move.effect:
                                # ADD CASE FOR DREAM EATER
                                #if move.name == 'dream-eater' and defender.status_condition == Status.ASLEEP
                                attacker.recover_hp(np.round(damage/2, 2))
                            elif 'max hp' in move.effect:
                                attacker.recover_hp(np.round(attacker.base_hp/2, 2))


                case 'status':
                    self.calculate_status(move, attacker, defender)
                case _:
                    pass
        else:
            print(f'{attacker.name.upper()}\'s move missed')

    def calculate_damage(self, move: Move, attacker: Pokemon, defender: Pokemon, damage_override=-1):
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

        if damage_override == -1:
            damage = np.round(base * stab * type_effect * random_val, 2)
        else:
            damage = damage_override
        print('\tDAMAGE: ', damage)

        if type_effect >= 2.0:
            print('\tIt\'s super effective!')
        elif type_effect == 0.5:
            print('\tIt\'s not very effective')
        elif type_effect == 0:
            print('\tIt has no effect')

        return damage
    
    def calculate_status(self, move: Move, attacker: Pokemon, defender: Pokemon):
        effect_segments = move.effect.split('and')

        for effect in effect_segments:
            if 'sharply raises' in effect:
                if 'attack' in effect:
                    attacker.modifiy_stats_stage('attack', 2)
                elif 'defense' in effect and 'special defense' not in effect:
                    attacker.modifiy_stats_stage('defense', 2)
                elif 'special attack' in effect:
                    attacker.modifiy_stats_stage('sp_atk', 2)
                elif 'special defense' in effect:
                    attacker.modifiy_stats_stage('sp_def', 2)
                elif 'speed' in effect:
                    attacker.modifiy_stats_stage('speed', 2)
                elif 'evasiveness' in effect:
                    attacker.modifiy_stats_stage('evasiveness', 2)
                elif 'accuracy' in effect:
                    attacker.modifiy_stats_stage('accuracy', 2)
            elif 'sharply lowers' in effect:
                if 'attack' in effect:
                    defender.modifiy_stats_stage('attack', -2)
                elif 'defense' in effect and 'special defense' not in effect:
                    defender.modifiy_stats_stage('defense', -2)
                elif 'special attack' in effect:
                    defender.modifiy_stats_stage('sp_atk', -2)
                elif 'special defense' in effect:
                    defender.modifiy_stats_stage('sp_def', -2)
                elif 'speed' in effect:
                    defender.modifiy_stats_stage('speed', -2)
                elif 'evasiveness' in effect:
                    defender.modifiy_stats_stage('evasiveness', -2)
                elif 'accuracy' in effect:
                    defender.modifiy_stats_stage('accuracy', -2)
            elif 'raises' in effect:
                if 'attack' in effect:
                    attacker.modifiy_stats_stage('attack', 1)
                elif 'defense' in effect and 'special defense' not in effect:
                    attacker.modifiy_stats_stage('defense', 1)
                elif 'special attack' in effect:
                    attacker.modifiy_stats_stage('sp_atk', 1)
                elif 'special defense' in effect:
                    attacker.modifiy_stats_stage('sp_def', 1)
                elif 'speed' in effect:
                    attacker.modifiy_stats_stage('speed', 1)
                elif 'evasiveness' in effect:
                    attacker.modifiy_stats_stage('evasiveness', 1)
                elif 'accuracy' in effect:
                    attacker.modifiy_stats_stage('accuracy', 1)
            elif 'lowers' in effect:
                if 'attack' in effect:
                    defender.modifiy_stats_stage('attack', -1)
                elif 'defense' in effect and 'special defense' not in effect:
                    defender.modifiy_stats_stage('defense', -1)
                elif 'special attack' in effect:
                    defender.modifiy_stats_stage('sp_atk', -1)
                elif 'special defense' in effect:
                    defender.modifiy_stats_stage('sp_def', -1)
                elif 'speed' in effect:
                    defender.modifiy_stats_stage('speed', -1)
                elif 'evasiveness' in effect:
                    defender.modifiy_stats_stage('evasiveness', -1)
                elif 'accuracy' in effect:
                    defender.modifiy_stats_stage('accuracy', -1)
            elif 'confuses' in effect:
                defender.add_confused(random.randint(2, 5))
            elif 'paralyzes' in effect:
                defender.add_status(Status.PARALYZED)
            elif 'opponent to sleep' in effect:
                defender.add_status(Status.ASLEEP, status_count=random.randint(1,7))
            elif 'poisons' in effect:
                defender.add_status(Status.POISONED)

    def apply_status_effects(self, pokemon: Pokemon):
        lose_turn = False

        if pokemon.is_confused:
            pokemon.confused_count += 1
            if pokemon.curr_confused_count == pokemon.confused_count:
                pokemon.remove_confused()
                print(f'{pokemon.name.upper()} snapped out of confusion!')
            else:
                print(f'\t{pokemon.name.upper()} is confused')
                if random.random() <= 0.5:
                    print(f'\t{pokemon.name.upper()} hurt itself in it\'s confusion')
                    confusion_damage_move = Move(
                        name='confusion-damage',
                        type='*',
                        power=40,
                        accuracy=100,
                        category='physical',
                        pp=25,
                        effect='confusion damage'
                    )
                    confusion_damage = self.calculate_damage(confusion_damage_move, pokemon, pokemon)
                    pokemon.reduce_hp(confusion_damage)
                    lose_turn = True

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
                    lose_turn = False
                    pokemon.remove_status()
                    print(f'\t{pokemon.name.upper()} woke up!')
                else:
                    pokemon.curr_status_count += 1
                    lose_turn = True
                    print(f'\t{pokemon.name.upper()} is asleep')
            case Status.POISONED:
                pokemon.reduce_hp(pokemon.base_hp/16)
                print(f'\t{pokemon.name.upper()} was hurt by poison')
            case Status.BURNED:
                pokemon.attack *= 0.5
                pokemon.reduce_hp(pokemon.base_hp/16)
                print(f'\t{pokemon.name.upper()} was hurt by its burn')
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
        filled = int(hp_ratio * 15)
        empty = 15 - filled

        status = status_icon['confused'] if self.player_pokemon.is_confused else '' + status_icon[self.player_pokemon.status]

        print(f"{self.player_pokemon.name.upper():<12}\t[{'█' * filled}{'-' * empty}] {status} HP {self.player_pokemon.curr_hp}/{self.player_pokemon.base_hp}")

        hp_ratio = self.opp_pokemon.curr_hp / self.opp_pokemon.base_hp
        filled = int(hp_ratio * 15)
        empty = 15 - filled

        status = status_icon['confused'] if self.opp_pokemon.is_confused else '' + status_icon[self.opp_pokemon.status]

        print(f"{self.opp_pokemon.name.upper():<12}\t[{'█' * filled}{'-' * empty}] {status} HP {self.opp_pokemon.curr_hp}/{self.opp_pokemon.base_hp}")



    

    