from pokemon import Pokemon
from moves import Move
import random
import numpy as np
import pandas as pd

'''

- none

- 'may'
    - 'lower'
        - 'special defense'
        - 'defense'
        - 'special attack'
        - 'attack'
        - 'accuracy'
        - 'evasiveness'
    - 'raise'
    - 'flinching'
    - 'freeze'
    - 'paralyze'
    - 'confuse'
    - 'burn'
    - 'poison'
    - 'to sleep'

- 'raises' and not 'sharply raises'
    - 'special defense'
    - 'defense'
    - 'special attack'
    - 'attack'
    - 'accuracy'
    - 'evasiveness'

- 'lowers' and not 'sharply lowers'
    - 'special defense'
    - 'defense'
    - 'special attack'
    - 'attack'
    - 'accuracy'
    - 'evasiveness'

'sharply lowers':
    - 'special defense'
    - 'defense'
    - 'special attack'
    - 'attack'
    - 'accuracy'
    - 'evasiveness'

'sharply raises'
    - 'special defense'
    - 'defense'
    - 'special attack'
    - 'attack'
    - 'accuracy'
    - 'evasiveness'

- 'confuses'

- 'paralyzes'

- 'opponents to sleep'

- 'poisons'

- 'badly poisons'

- 'user sleeps'
    
'recovers'
    - 'half the hp inflicted'
        - 'sleeping'
    - 'max hp'
        - 'half its max hp'

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

- 'hits' and 'in one turn'
    - '2-5 times'
    - 'twice'

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

- 'resets'
    - 'all stat changes'
    - 'opponent's evasiveness' and 'allows normal' and 'fighting' and 'to hit ghosts'

- 'recoil'

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

- 'always inflicts'
    - '40 HP'
    - '20 HP'

- 'inflicts damage'
    - '50-150% of user's level'
    - 'equal to the user's remaining HP'
    - 'equal to user's level'
    - 'based on the target's defense, not special defense'
    - 'equal to user's level'
    - 'on contact'

- 'inflict double damage'
    - 'poisoned'
    - 'if the target has a status condition'
    - 'if a teammate fainted on the last turn'

- 'faints'
    - 'user faints'
        - 'opponent also faints'
        - 'pp for opponent's last move is depleted'
        - 'next pokémon released is fully healed'
        - 'sharply lowers opponent's attack and special attack'
    - 'in 3 turns'

- 'one-hit ko'

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

- 'random'
    - 'any move in the game'
    - 'power'

- 'stats cannot be changed'

- 'user attacks for 2-3 turns' or 'user attacks for 3 turns'
    - 'then becomes confused'
    - 'prevents sleep'

- 'the opponent switches'

- 'doesnt do anything' or 'warps player to last pokécenter'

- 'decoy'

- 'always takes off half of the opponent's hp'

- 'user takes on the form and attacks of the opponent'

'''

def handle_move_effects(move: Move, attacker: Pokemon, defender: Pokemon):

    if 'none' in move.name:
        print('no special effects')
        damage = calculate_damage(move, attacker, defender)
        defender.reduce_hp(damage)
        return


    if 'may' in move.name:
        pass

    if 'raises' in move.name and not 'sharply raises' in move.name:
        pass

    if 'lowers' in move.name and not 'sharply lowers' in move.name:
        pass

    if 'sharply raises' in move.name:
        pass

    if 'sharply lowers' in move.name:
        pass

    if 'confuses' in move.name:
        pass

    if 'paralyzes' in move.name:
        pass

    if 'opponents to sleep' in move.name:
        pass

    if 'poisons' in move.name:
        pass

    if 'badly poisons' in move.name:
        pass

    if 'user sleeps' in move.name:
        pass

    if 'recovers' in move.name:
        pass

    if 'drains hp' in move.name:
        pass

    if 'traps' in move.name:
        pass

    if 'next turn' in move.name:
        pass

    if 'on first turn' in move.name and 'attacks on second' in move.name:
        pass

    if 'critical hit ratio' in move.name:
        pass

    if 'hits' in move.name and 'in one turn' in move.name:
        pass

    if 'ignores' in move.name:
        pass

    if 'user attacks first' in move.name:
        pass

    if 'when hit' in move.name:
        pass

    if 'last' in move.name:
        pass

    if 'resets' in move.name:
        pass

    if 'recoil' in move.name:
        pass

    if 'user takes damage for two turns then strikes back double' in move.name:
        pass

    if 'power is doubled if' in move.name or 'power doubles if' in move.name or 'doubles in power' in move.name or 'double power' in move.name:
        pass

    if 'user\'s type' in move.name:
        pass

    if 'always inflicts' in move.name:
        pass

    if 'inflicts damage' in move.name:
        pass

    if 'inflicts double damage' in move.name:
        pass

    if 'faints' in move.name:
        pass

    if 'one-hit ko' in move.name:
        pass

    if 'if it misses' in move.name:
        pass

    if 'halves':
        pass

    if 'the heavier':
        pass

    if 'random':
        pass

    if 'stats cannot be changed':
        pass

    if 'user attacks for 2-3 turns' in move.name or 'user attacks for 3 turns' in move.name:
        pass

    if 'the opponent switches' in move.name:
        pass

    if 'doesnt do anything' in move.name or 'warps player to last pokécenter' in move.name:
        pass

    if 'decoy' in move.name:
        pass

    if 'always takes off half of the opponent\'s hp' in move.name:
        pass

    if 'user takes on the form and attacks of the opponent' in move.name:
        pass




def calculate_damage(self, move: Move, attacker: Pokemon, defender: Pokemon, damage_override=-1):
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

    if damage_override == -1:
        damage = np.round(base * stab * type_effect * random_val, 2)
    else:
        damage = damage_override
    print('DAMAGE: ', damage)

    if type_effect >= 2.0:
        print('It\'s super effective!')
    elif type_effect == 0.5:
        print('It\'s not very effective')
    elif type_effect == 0:
        print('It has no effect')

    return damage
