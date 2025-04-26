from pokemon import Pokemon
from battle_env import BattleEnv
import moves
import random
import numpy as np
import main_helper
import time

# 881140 Caterpie vs Metapod
# 728127 instant Self-Destruct
# 679815 interesting battle Hitmonlee vs Chansey
# seed = random.randint(0, 1000000)
# main_helper.set_seed(seed)

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
    seed = random.randint(0, 1000000)
    main_helper.set_seed(seed)

    agent_pokemon = Pokemon(random.randint(1, 151), version) # 4 for charmander
    agent_pokemon.print_data()

    opp_pokemon = Pokemon(random.randint(1, 151), version) # 7 for squirtle
    opp_pokemon.print_data()

    env = BattleEnv(agent_pokemon, opp_pokemon)

    env.start_battle()

end = time.time()
elapsed = end - start
print(f'executed {episodes} episodes in {elapsed:.2f} seconds')

