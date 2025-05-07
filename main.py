from pokemon import Pokemon
from battle_env import BattleEnv
from trainer import Trainer
import moves
import random
import numpy as np
import main_helper
import time

# 957405: Kadabra sweeps Gary's entire team in 1 turn? (party_size=3)
# 604053: Hitmonchan hits Chansey with thunder-punch for 513 damage? (party_size=3)
seed = 471433#random.randint(0, 1000000)
main_helper.set_seed(seed)


start = time.time()


version = 'red-blue'
party_size = 3
episodes = 1

outcomes = []
for i in range(episodes):

    user = Trainer('ASH', version, party_size=party_size)
    opp = Trainer('GARY', version, party_size=party_size)

    env = BattleEnv(user, opp)

    # 1 for user win, 0 for opp win
    outcome = env.simulate_battle()
    outcomes.append(outcome)


print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
print(f'USER WIN-RATE: {np.mean(outcomes)*100}% ({np.sum(outcomes)}/{len(outcomes)})')    

end = time.time()
elapsed = end - start
print(f'simulated {episodes} battle(s) in {elapsed:.2f} seconds')

