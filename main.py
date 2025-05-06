from pokemon import Pokemon
from battle_env import BattleEnv
from trainer import Trainer
import moves
import random
import numpy as np
import main_helper
import time

version = 'red-blue'
episodes = 1

start = time.time()

for i in range(episodes):
    # 881140 Caterpie vs Metapod
    # 728127 instant Self-Destruct
    # 679815 interesting battle Hitmonlee vs Chansey
    # 349356 epic comeback Wigglytuff vs Vileplume
    # 98368  weird out-of-order effect with confusion and fainting
    # 557439 weird out-of-order effect with poisoning and fainting
    # 398256 vileplume never snaps out of confusion
    # 313455 use of Metronome
    # 272224 uses of Metronome that randomly selects Metronome again
    # 843007 both pokemon faint on the last turn
    seed = random.randint(0, 1000000)
    main_helper.set_seed(seed)

    user = Trainer('ASH', version)
    opp = Trainer('GARY', version)

    # Each side throws out the first pokemon in their party (randomly chosen)
    user_pokemon = Pokemon(user.party[0].id, version)
    user_pokemon.print_data()

    opp_pokemon = Pokemon(opp.party[0].id, version)
    opp_pokemon.print_data()

    env = BattleEnv(user_pokemon, opp_pokemon)

    env.start_battle()

end = time.time()
elapsed = end - start
print(f'executed {episodes} episodes in {elapsed:.2f} seconds')

