from pokemon import Pokemon
from moves import Move
import random
import numpy as np
import pandas as pd
from pokemon_enums import Status
from moves import moves_db


# FINISHED
################################################
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

- 'badly poisons'

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
        if 'any move in the game' in move.effect: # Only applies to Metronome
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
        if 'lower' in move.effect:
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


    if 'raises' in move.effect and not 'sharply raises' in move.effect and 'when hit' not in move.effect and 'first turn' not in move.effect:
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
            if 'sleeping' in move.effect: # for Dream Eater
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
            attacker.temp_effects['drains_hp'] = {'move': move.name, 'turns_left': -1, 'effect': 'opp loses 1/8 max hp, user recovers it'}
            print('TODO: drains hp')
        else:
            print('the move had no effect')

    if 'traps' in move.effect:
        defender.temp_effects['trapped'] = {'move': move.name, 'turns_left': random.choice([4, 5])}
        print(f'{defender.name.upper()} has become trapped!')
        print('TODO: traps')

    if 'next turn' in move.effect:
        if 'recharge' in move.effect:
            defender.temp_effects['recharge'] = {'move': move.name, 'turns_left': 1, 'effect': 'user loses turn'}

        if 'opponent to sleep' in move.effect:
            defender.temp_effects['opp_to_sleep'] = {'move': move.name, 'turns_left': 1, 'effect': 'opp sleeps'}

        print('TODO: next turn')

    if 'on first turn' in move.effect and 'attacks on second' in move.effect:
        attacker.temp_effects['attacks_on_second'] = {'move': move.name, 'turns_left': 1, 'effect': 'attacks'}
        damage = 0
        print(f'{attacker.name.upper()} {move.effect.split(' ')[0]}')
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
        print(f'Hit {hit_count} time(s)!')

    if 'ignores' in move.effect:
        print('TODO: ignores')
        pass

    if 'user attacks first' in move.effect:
        print('TODO: user attacks first')
        pass

    if 'when hit' in move.effect:
        if 'raises user\'s attack' in move.effect:
            attacker.temp_effects['when_hit'] = {'move': move.name, 'turns_left': -1, 'effect': 'raises attack'}

        if 'by a physical attack' in move.effect:
            attacker.temp_effects['when_hit_phys'] = {'move': move.name, 'turns_left': -1, 'effect': 'strikes back with 2x power'}

        if 'by a special attack' in move.effect:
            attacker.temp_effects['when_hit_sp'] = {'move': move.name, 'turns_left': -1, 'effect': 'strikes back with 2x power'}

        print('TODO: when hit')
        pass

    if 'last' in move.effect:
        print('TODO: last')

        if 'opponent can\'t use its last attack for a few turns' in move.effect:
            defender.temp_effects[f'disable_{defender.move_history[-1]}'] = {'move': move.name, 'turns_left': 5, 'effect': f'opp can\'t use {defender.move_history[-1]} for 5 turns'}
            print(f'TODO: {defender.name.upper()} had {defender.move_history[-1]} disabled')

        if 'forces opponent to keep using its last move for 3 turns' in move.effect:
            defender.temp_effects[f'encore_{defender.move_history[-1]}'] = {'move': move.name, 'turns_left': 3, 'effect': f'opp must use {defender.move_history[-1]} for 3 turns'}
            print(f'TODO: {defender.name.upper()} is forced to use {defender.move_history[-1]}')

        if 'copies the opponent\'s last move' in move.effect or 'user performs the opponent\'s last move' in move.effect:
            move = defender.move_history[-1]
            damage = calculate_damage(move, attacker, defender)
            print(f'{attacker.name.upper()} copied {defender.name.upper()} and used {move.name.upper()}')

        if ' pp' in move.effect:
            print('TODO: handle last move PP reduction')
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
        attacker.temp_effects['bide'] = {'move': move.name, 'turns_left': 2, 'effect': 'attacks with damage_stored*2'}
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
            damage = 40
        elif '20 hp' in move.effect:
            damage = 20

    if 'inflicts damage' in move.effect:
        if f'50-150% of user\'s level' in move.effect:
            damage = np.round(attacker.level*random.uniform(0.5, 1.5), 1)

        if 'equal to the user\'s remaining HP' in move.effect:
            damage = attacker.curr_hp

        if 'equal to user\'s level' in move.effect:
            damage = attacker.level

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
            print('TODO: if a teammate fainted on the last turn')
            pass

    if 'faints' in move.effect:
        attacker.reduce_hp(attacker.curr_hp)
        print('TODO: faints')
        pass

    if 'one-hit-ko' in move.effect:
        damage = defender.curr_hp
        print(f'{defender.name.upper()} was one-hit KO\'d!')

    if 'if it misses' in move.effect:
        print('TODO: if it misses')
        pass

    if 'halves' in move.effect:
        if 'damage' in move.effect:
            if 'physical and special attacks' in move.effect:
                attacker.temp_effects['halves_phys_spatk'] = {'move': move.name, 'turns_left': 5, 'effect': 'halves damage from physical and special attacks'}
                pass

            if 'special attacks' in move.effect and 'physical' not in move.effect:
                attacker.temp_effects['halves_spatk'] = {'move': move.name, 'turns_left': 5, 'effect': 'halves damage from special attacks'}
                pass

            if 'physical attacks' in move.effect:
                attacker.temp_effects['halves_phys'] = {'move': move.name, 'turns_left': 5, 'effect': 'halves damage from physical attacks'}
                pass
        
        if 'foe\'s hp' in move.effect:
            damage = defender.curr_hp / 2

        print('TODO: halves')
        pass

    if 'the heavier' in move.effect:
        print('TODO: the heavier')
        pass

    if 'stats cannot be changed' in move.effect:
        attacker.temp_effects['no_stats_change'] = {'move': move.name, 'turns_left': 5, 'effect': 'no status effects'}
        print('TODO: stats cannot be changed')
        pass

    if 'user attacks for 2-3 turns but then becomes confused' in move.effect:
        turns = random.choice([2, 3])
        attacker.temp_effects['attack_then_confusion'] = {'move': move.name, 'turns_left': turns, 'effect': 'user becomes confused'}
        print('TODO: user attacks for 2-3 turns then becomes confused')
        pass

    if 'user attacks for 3 turns and prevents sleep' in move.effect:
        attacker.temp_effects['attack_and_prevent_sleep'] = {'move': move.name, 'turns_left': 3, 'effect': 'user cant sleep'}
        print('TODO: user attacks for 3 turns and prevents sleep (and wakes up)')
        pass

    if 'the opponent switches' in move.effect:
        print('TODO: the opponent switches')
        pass

    if 'doesn\'t do anything' in move.effect or 'warps player to last pokécenter' in move.effect:
        damage = 0
        print('nothing happened')

    if 'decoy' in move.effect:
        attacker.temp_effects['decoy'] = {'move': move.name, 'turns_left': -1, 'effect': 'uses HP to create a decoy'}
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




def calculate_damage(move: Move, attacker: Pokemon, defender: Pokemon):
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

    damage = np.round(base * stab * type_effect * random_val, 2) if move.power > -1 else 0
        
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

def apply_status_effects(pokemon: Pokemon):
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
                confusion_damage = calculate_damage(confusion_damage_move, pokemon, pokemon)
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


def apply_temp_effects(attacker: Pokemon, defender: Pokemon):
    lose_turn = False
    effects_to_remove = []

    if attacker.temp_effects == {}:
        print(f'{attacker.name.upper()} has no temp_effects')
    else:
        for key,value in attacker.temp_effects.items():
            print(f'analyzing {key}')

            if key == 'bide':
                lose_turn = True
                value['turns_left'] -= 1
                if value['turns_left'] > 0:
                    print(f'{attacker.name.upper()} is storing energy')
                else:
                    damage = np.sum(attacker.damage_history[-2:]) * 2  # sum damage inflicted over last 2 turns and multiply by 2
                    print('bide damage:', attacker.damage_history[-2:])
                    defender.reduce_hp(damage)
                    effects_to_remove.append(key)
                    print(f'{attacker.name.upper()} unleashes energy: ({damage} Damage)!')
            # elif key == 'attack_on_second':
                # lose_turn = True
                # value['turns_left'] -= 1
                # if value['turns_left'] > 0:



    for effect in effects_to_remove:
        del attacker.temp_effects[effect]


    return lose_turn



def get_hit_chance(move: Move, attacker: Pokemon, defender: Pokemon):
    accuracy_stage_multipliers = {
        -6: 0.33, -5: 0.375, -4: 0.43, -3: 0.5, -2: 0.6, -1: 0.75,
            0: 1.0,  1: 1.33,   2: 1.66,  3: 2.0,  4: 2.33,  5: 2.66, 6: 3.0
    }

    accuracy = accuracy_stage_multipliers[attacker.accuracy_tier]
    evasiveness= accuracy_stage_multipliers[defender.evasiveness_tier]
    base = 100 if move.accuracy == -1 else move.accuracy / 100.0
    return base * (accuracy / evasiveness)
