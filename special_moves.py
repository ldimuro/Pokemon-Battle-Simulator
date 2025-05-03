from pokemon import Pokemon
from moves import Move
import random
import numpy as np
import pandas as pd
from pokemon_enums import Status
from moves import moves_db

# - none

# - 'may'
#     - 'lower'
#         - 'special defense'
#         - 'defense'
#         - 'special attack'
#         - 'attack'
#         - 'accuracy'
#         - 'evasiveness'
#     - 'raise'
#     - 'flinching'
#     - 'freeze'
#     - 'paralyze'
#     - 'confuse'
#     - 'burn'
#     - 'poison'
#     - 'to sleep'

# - 'raises' and not 'sharply raises'
#     - 'special defense'
#     - 'defense'
#     - 'special attack'
#     - 'attack'
#     - 'accuracy'
#     - 'evasiveness'

# - 'lowers' and not 'sharply lowers'
#     - 'special defense'
#     - 'defense'
#     - 'special attack'
#     - 'attack'
#     - 'accuracy'
#     - 'evasiveness'

# 'sharply lowers':
#     - 'special defense'
#     - 'defense'
#     - 'special attack'
#     - 'attack'
#     - 'accuracy'
#     - 'evasiveness'

# 'sharply raises'
#     - 'special defense'
#     - 'defense'
#     - 'special attack'
#     - 'attack'
#     - 'accuracy'
#     - 'evasiveness'

# - 'confuses'

# - 'paralyzes'

# - 'opponents to sleep'

# - 'poisons'

# - 'badly poisons'

# - 'user sleeps'
    
# 'recovers'
#     - 'half the hp inflicted'
#         - 'sleeping'
#     - 'max hp'
#         - 'half its max hp'

# - 'recoil'

# - 'one-hit ko'

# - 'always takes off half of the opponent's hp'

# - 'user takes on the form and attacks of the opponent'

# - 'doesnt do anything' or 'warps player to last pokécenter'

# - 'random'
#     - 'any move in the game'
#     - 'power'

# - 'resets'
#     - 'all stat changes'
#     - 'opponent's evasiveness' and 'allows normal' and 'fighting' and 'to hit ghosts'

# - 'always inflicts'
#     - '40 HP'
#     - '20 HP'

# - 'inflict double damage'
#     - 'poisoned'
#     - 'if the target has a status condition'
#     - 'if a teammate fainted on the last turn'

# - 'hits' and 'in one turn'
#     - '2-5 times'
#     - 'twice'

'''

- 'may'
    - 'flinching'

- 'drains hp'

- 'traps'
    - 'damaging them for 4-5 turns'

- 'next turn'
    - 'recharge'
    - 'opponent to sleep'

- 'on first turn' and 'attacks on second'
    - 'charges'
    - 'digs'
    - 'flies up'
    - 'springs up'
    - 'dives'
    - 'raises defense'

- 'critical hit ratio'
    - 'increases'
    - 'high'

- 'ignores'
    - 'accuracy and evasiveness'
    - 'opponent's stat changes'
    - 'target's ability'

- 'user attacks first'

- 'when hit'
    - 'raises user's attack'
    - 'by a physical attack'
    - 'by a special attack

- 'last' (lots of variations here)
    - 'attack for a few turns'
    - 'move'
        - 'copies'
        - 'PP'
        - 'performs'


- 'user takes damage for two turns then strikes back double'

- 'power is doubled if' or 'power doubles if' or 'doubles in power' or 'double power'
    - 'underground from using dig'
    - 'opponent already took damage in the same turn'
    - 'user took damage first'
    - 'opponent's HP is less than 50%'
    - 'user is burned, poisoned, or paralyzed'
    - 'user was attacked first'
    - 'each turn for 5 turns'
    - 'opponent is paralyzed, but cures it'
    - 'opponent is asleep, but wakes it up'
    - 'fly/bounce/sky drop'

- 'user's type'
    - 'it's first move'
    - 'to the location'

- 'inflicts damage'
    - '50-150% of user's level'
    - 'equal to the user's remaining HP'
    - 'equal to user's level'
    - 'based on the target's defense, not special defense'
    - 'on contact'


- 'faints'
    - 'user faints'
        - 'opponent also faints'
        - 'pp for opponent's last move is depleted'
        - 'next pokémon released is fully healed'
        - 'sharply lowers opponent's attack and special attack'
    - 'in 3 turns'



- 'if it misses'

- 'halves'
    - 'damage'
        - 'physical and special attacks'
        - 'special attacks' and not 'physical'
        - 'physical attacks'
    - 'foe's hp'

- 'the heavier'
    - 'opponent'
    - 'user'


- 'stats cannot be changed'

- 'user attacks for 2-3 turns' or 'user attacks for 3 turns'
    - 'then becomes confused'
    - 'prevents sleep'

- 'the opponent switches'


- 'decoy'



'''

def handle_move_effects(move: Move, attacker: Pokemon, defender: Pokemon):

    if 'none' in move.effect:
        print('no special effects')
        damage = calculate_damage(move, attacker, defender)
        defender.reduce_hp(damage)
        return
    
    if 'random' in move.effect:
        if 'any move in the game' in move.effect: # Only applies to metronome
            _, move = random.choice(list(moves_db.items()))
            print(f'{attacker.name.upper()} randomly uses {move.name.upper()}')
        elif 'power' in move.effect: # Only applies to magnitude
            magnitude_powers = {4: (0.05, 10), 5: (0.1, 30), 6: (0.2, 50), 7: (0.3, 70), 
                                8: (0.2, 90), 9: (0.1, 110), 10: (0.05, 150)}
            keys = list(magnitude_powers.keys())
            weights = [magnitude_powers[k][0] for k in keys]

            random_val = random.choices(keys, weights=weights)[0]
            print(f'Magnitude {random_val}!')

            # Add extra damage is opponent has used Dig
            print('TODO: handle Magnitude case')

            # damage = calculate_damage(move, attacker, defender, damage_override=magnitude_powers[random_val][1])


    damage = calculate_damage(move, attacker, defender)


    if 'may' in move.effect:
        if 'lower':
            if random.random() <= 0.1:
                handle_stat_change(move, defender, -1)

        if 'raise' in move.effect:
            if random.random() <= 0.1:
                handle_stat_change(move, attacker, 1)

        if 'paralyze, burn, or freeze' in move.effect:
            if random.random() <= 0.2:
                defender.add_status(random.choice([Status.PARALYZED, Status.BURNED, Status.FROZEN]))

        if 'flinching' in move.effect:
            print('TODO: may cause flinching')
            pass

        if 'freeze' in move.effect:
            if random.random() <= 0.1:
                defender.add_status(Status.FROZEN)

        if 'paralze' in move.effect:
            if move.name == 'thunder' or move.name == 'body-slam':
                if random.random() <= 0.3:
                    defender.add_status(Status.PARALYZED)
            else:
                if random.random() <= 0.1:
                    defender.add_status(Status.PARALYZED)

        if 'confuse' in move.effect:
            if move.name == 'dizzy-punch':
                if random.random() <= 0.2:
                    defender.add_confused(random.randint(2, 5))
            else:
                if random.random() <= 0.1:
                    defender.add_confused(random.randint(2, 5))

        if 'burn' in move.effect:
            if random.random() <= 0.1:
                defender.add_status(Status.BURNED)

        if 'poison' in move.effect:
            if move.name == 'twineedle':
                if random.random() <= 0.2:
                    defender.add_status(Status.POISONED)
            elif move.name == 'smog':
                if random.random() <= 0.4:
                    defender.add_status(Status.POISONED)
            else:
                if random.random() <= 0.3:
                    defender.add_status(Status.POISONED)


    if 'raises' in move.effect and not 'sharply raises' in move.effect and 'when hit' not in move.effect:
        handle_stat_change(move, attacker, 1)

    if 'lowers' in move.effect and not 'sharply lowers' in move.effect:
        handle_stat_change(move, defender, -1)

    if 'sharply raises' in move.effect:
        handle_stat_change(move, attacker, 2)

    if 'sharply lowers' in move.effect:
        handle_stat_change(move, defender, -2)

    if 'confuses' in move.effect:
        defender.add_confused(random.randint(2, 5))

    if 'paralyzes' in move.effect:
        defender.add_status(Status.PARALYZED)

    if 'opponent to sleep' in move.effect:
        defender.add_status(Status.ASLEEP, status_count=random.randint(1,7))

    if 'poisons' in move.effect:
        defender.add_status(Status.POISONED)

    if 'badly poisons' in move.effect:
        print('TODO: badly poisons')
        pass

    if 'user sleeps' in move.effect:
        if attacker.status is not Status.NONE:
            attacker.remove_status()

        attacker.add_status(Status.ASLEEP, 2)
        attacker.recover_hp(attacker.base_hp - attacker.curr_hp)

    if 'recovers' in move.effect:
        if 'half the hp inflicted' in move.effect:
            if 'sleeping' in move.effect:
                if defender.status == Status.ASLEEP:
                    attacker.recover_hp(np.round(damage/2, 2))
                else:
                    damage = 0
                    print('the move had no effect')
            else:
                attacker.recover_hp(np.round(damage/2, 2))
         
        if 'max hp' in move.effect:
            attacker.recover_hp(np.round(attacker.base_hp/2, 2))

    if 'drains hp' in move.effect:
        if 'grass' not in defender.types:
            attacker.temp_effects['drains_hp'] = {'move': move, 'turns_left': -1, 'effect': 'opp loses 1/8 max hp, user recovers it'}
            print('TODO: drains hp')
        else:
            print('the move had no effect')

    if 'traps' in move.effect:
        defender.temp_effects['trapped'] = {'move': move, 'turns_left': random.choice([4, 5])}
        print(f'{defender.name.upper()} has become trapped!')
        print('TODO: traps')

    if 'next turn' in move.effect:
        if 'recharge' in move.effect:
            defender.temp_effects['recharge'] = {'move': move, 'turns_left': 1, 'effect': 'user loses turn'}

        if 'opponent to sleep':
            defender.temp_effects['opp_to_sleep'] = {'move': move, 'turns_left': 1, 'effect': 'opp sleeps'}

        print('TODO: next turn')

    if 'on first turn' in move.effect and 'attacks on second' in move.effect:
        attacker.temp_effects['attacks_on_second'] = {'move': move, 'turns_left': 1, 'effect': 'attacks'}
        damage = 0
        print(f'{attacker.name.upper()} {move.effect[0]}')
        print('TODO: on first turn, attacks on second')
        pass

    if 'critical hit ratio' in move.effect:
        print('TODO: critical hit ratio')
        pass

    if 'hits' in move.effect and 'in one turn' in move.effect:
        if '2-5 times' in move.effect:
            hit_count = random.choices([2, 3, 4, 5], weights=[37.5, 37.5, 12.5, 12.5])[0]
        elif 'twice' in move.effect:
            hit_count = 2

        for hit_num in range(hit_count):
            damage = calculate_damage(move, attacker, defender)
            defender.reduce_hp(damage)
            print('DAMAGE: ', damage)
        print(f'Hit {hit_count} times!')
        return

    if 'ignores' in move.effect:
        print('TODO: ignores')
        pass

    if 'user attacks first' in move.effect:
        print('TODO: user attacks first')
        pass

    if 'when hit' in move.effect:
        if 'raises user\'s attack':
            attacker.temp_effects['when_hit'] = {'move': move, 'turns_left': -1, 'effect': 'raises attack'}

        if 'by a physical attack':
            attacker.temp_effects['when_hit_phys'] = {'move': move, 'turns_left': -1, 'effect': 'strikes back with 2x power'}

        if 'by a special attack':
            attacker.temp_effects['when_hit_sp'] = {'move': move, 'turns_left': -1, 'effect': 'strikes back with 2x power'}

        print('TODO: when hit')
        pass

    if 'last' in move.effect:
        print('TODO: last')
        pass

    if 'resets' in move.effect:
        if 'all stat changes' in move.effect:
            stats = ['attack', 'defense', 'sp_atk', 'sp_def', 'speed', 'evasiveness', 'accuracy']
            pokemon = [attacker, defender]
            for mon in pokemon:
                for stat in stats:
                    mon.reset_stat(stat)
        elif 'opponent\'s evasiveness' in move.effect and 'allows normal' in move.effect and 'fighting' in move.effect and 'to hit ghosts' in move.effect:
            print('TODO: handle case')

    if 'recoil' in move.effect:
        recoil_damage = np.floor(damage / 4)
        attacker.reduce_hp(recoil_damage)
        print(f'{attacker.name.upper()} took recoil damage')

    if 'user takes damage for two turns then strikes back double' in move.effect:
        attacker.temp_effects['bide'] = {'move': move, 'turns_left': 2, 'effect': 'attacks with damage_stored*2', 'damage_stored': 0}
        print('TODO: user takes damage for two turns then strikes back double')
        pass

    if 'power is doubled if' in move.effect or 'power doubles if' in move.effect or 'doubles in power' in move.effect or 'double power' in move.effect:
        print('TODO: power is doubled')
        pass

    if 'user\'s type' in move.effect:
        print('TODO: user\'s type')
        pass

    if 'always inflicts' in move.effect:
        if '40 hp' in move.effect:
            damage = calculate_damage(move, attacker, defender, damage_override=40)
        elif '20 hp' in move.effect:
            damage = calculate_damage(move, attacker, defender, damage_override=20)

    if 'inflicts damage' in move.effect:
        if f'50-150% of user\'s level' in move.effect:
            damage = calculate_damage(move, attacker, defender, damage_override=np.round(attacker.level*random.uniform(0.5, 1.5), 1))

        if 'equal to the user\'s remaining HP' in move.effect:
            damage = calculate_damage(move, attacker, defender, damage_override=attacker.curr_hp)

        if 'equal to user\'s level' in move.effect:
            damage = calculate_damage(move, attacker, defender, damage_override=attacker.level)

        if 'based on the target\'s defense, not special defense' in move.effect:
            print('TODO: based on the target\'s defense, not special defense')
            pass

        if 'on contact' in move.effect:
            print('TODO: on contact')
            pass

    if 'inflicts double damage' in move.effect:
        if 'poisoned' in move.effect and defender.status == Status.POISONED:
            damage *= 2
        
        if 'if the target has a status condition' in move.effect and defender.status != Status.NONE:
            damage *= 2

        if 'if a teammate fained on the last turn' in move.effect:
            print('TODO: if a teammate fained on the last turn')
            pass

    if 'faints' in move.effect:
        attacker.reduce_hp(attacker.curr_hp)
        print('TODO: faints')
        pass

    if 'one-hit ko' in move.effect:
        damage = defender.curr_hp
        print(f'{defender.name.upper()} was one-hit KO\'d!')

    if 'if it misses' in move.effect:
        print('TODO: if it misses')
        pass

    if 'halves' in move.effect:
        if 'damage' in move.effect:
            if 'physical and special attacks' in move.effect:
                attacker.temp_effects['halves_phys_spatk'] = {'move': move, 'turns_left': 5, 'effect': 'halves damage from physical and special attacks'}
                pass

            if 'special attacks' in move.effect and 'physical' not in move.effect:
                attacker.temp_effects['halves_spatk'] = {'move': move, 'turns_left': 5, 'effect': 'halves damage from special attacks'}
                pass

            if 'physical attacks' in move.effect:
                attacker.temp_effects['halves_phys'] = {'move': move, 'turns_left': 5, 'effect': 'halves damage from physical attacks'}
                pass
        
        if 'foe\'s hp' in move.effect:
            damage = defender.curr_hp / 2

        print('TODO: halves')
        pass

    if 'the heavier' in move.effect:
        print('TODO: the heavier')
        pass

    if 'stats cannot be changed' in move.effect:
        print('TODO: stats cannot be changed')
        pass

    if 'user attacks for 2-3 turns' in move.effect or 'user attacks for 3 turns' in move.effect:
        print('TODO: user attacks for 2-3, 3 turns')
        pass

    if 'the opponent switches' in move.effect:
        print('TODO: the opponent switches')
        pass

    if 'doesn\'t do anything' in move.effect or 'warps player to last pokécenter' in move.effect:
        damage = 0
        print('nothing happened')

    if 'decoy' in move.effect:
        print('TODO: decoy')
        pass

    if 'always takes off half of the opponent\'s hp' in move.effect:
        damage = defender.curr_hp / 2

    if 'user takes on the form and attacks of the opponent' in move.effect:
        attacker.moves = defender.moves
        attacker.types = defender.types
        print(f'{attacker.name.upper()} became type(s) {defender.types} with moves {[move.name for move in defender.moves]}')


    defender.reduce_hp(damage)
    print('DAMAGE: ', damage)

    

    return




def calculate_damage(move: Move, attacker: Pokemon, defender: Pokemon, damage_override=0):
    type_effectivenss_chart = pd.read_csv('type_effectiveness.csv', index_col=0)
    a = attacker.sp_atk if move.category == 'special' else attacker.attack
    d = defender.sp_def if move.category == 'special' else defender.defense
    stab = 1.5 if move.type in attacker.types else 1
    type1 = type_effectivenss_chart.loc[move.type, defender.types[0]]
    type2 = 1 if len(defender.types) == 1 else type_effectivenss_chart.loc[move.type, defender.types[1]]
    type_effect = type1 * type2
    random_val = random.randint(217, 255) / 255

    level_factor = (((2 * attacker.level * attacker.crit_ratio) / 5) + 2)
    base = ((level_factor * move.power * (a / d)) / 50) + 2

    if move.power == -1:
        damage = 0
    else:
        damage = np.round(base * stab * type_effect * random_val, 2)

    if damage_override > 0:
        damage = damage_override
    
        
    if move.category != 'status':
        if type_effect >= 2.0:
            print('It\'s super effective!')
        elif type_effect == 0.5:
            print('It\'s not very effective')
        elif type_effect == 0:
            print('It has no effect')

    return damage


def handle_stat_change(move: Move, pokemon: Pokemon, change):
    if 'attack' in move.effect and 'special attack' not in move.effect:
        pokemon.modifiy_stats_stage('attack', change)

    if 'special attack' in move.effect:
        pokemon.modifiy_stats_stage('sp_atk', change)

    if 'defense' in move.effect and not 'special defense' in move.effect:
        pokemon.modifiy_stats_stage('defense', change)

    if 'special defense' in move.effect:
        pokemon.modifiy_stats_stage('sp_def', change)

    if 'speed' in move.effect:
        pokemon.modifiy_stats_stage('speed', change)

    if 'accuracy' in move.effect:
        pokemon.modifiy_stats_stage('accuracy', change)

    if 'evasiveness' in move.effect:
        pokemon.modifiy_stats_stage('evasiveness', change)
