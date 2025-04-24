import random
import numpy
from pokemon import Pokemon
from moves import Move

class BattleEnv:
    def __init__(self, curr_pokemon: Pokemon, opp_pokemon: Pokemon):
        self.player_pokemon = curr_pokemon
        self.opp_pokemon = opp_pokemon

        print(f'{self.player_pokemon.name.upper()} ({self.player_pokemon.curr_hp} HP) vs. {self.opp_pokemon.name.upper()} ({self.opp_pokemon.curr_hp} HP)')

    def start_battle(self):
        
        count = 1
        while self.player_pokemon.curr_hp > 0 and self.opp_pokemon.curr_hp > 0:
            print(f'TURN {count} -----------------------------------------------------------------------')
            if count == 2:
                break

            player_move: Move = self.player_pokemon.use_move()
            opp_move: Move = self.opp_pokemon.use_move()

            if self.player_pokemon.speed >= self.opp_pokemon.speed:
                first_pokemon, first_move = self.player_pokemon, player_move
                second_pokemon, second_move = self.opp_pokemon, opp_move
            else:
                first_pokemon, first_move = self.opp_pokemon, opp_move
                second_pokemon, second_move = self.player_pokemon, player_move

            # First Move
            self.execute_move(first_move, first_pokemon, second_pokemon)

            # Second Move
            self.execute_move(second_move, second_pokemon, first_pokemon)







            count += 1


    def execute_move(self, move: Move, attacker: Pokemon, defender: Pokemon):
        print(f'{attacker.name.upper()} uses {move.name.upper()} on {defender.name.upper()}')


    

    