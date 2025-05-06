import random
import numpy as np

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    print(f'seed={seed}')

version_pokemon_range = {
    'red-blue': 151,
    'gold-silver': 251,
    'ruby-sapphire': 386,
    'diamond-pearl': 493
}