import uuid
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .utils.services import RandomNumberService

from .forms import GuessForm


class Game:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.winning_combination = []
        self.game_state = {}  # Initialize an empty game state

    # decorator indicates that this method does not need an instance of the class to be called and lets you load a game state from cache without needing an existing 'Game' Object.
    @staticmethod
    def load_game_state(game_id):
        game_state = cache.get(game_id)
        if game_state:
            game = Game()
            game.game_id = game_id
            game.game_state = game_state
            game.winning_combination = game_state['winning_combination']
            return game
        return None

    def save_game(self):
        cache.set(self.game_id, self.game_state, timeout=3600)

    def init_game_state(self):
        '''
        Initializes the game state.
        '''
        return {
            'last_guess': [],
            'attempts': 0,
            'win_state': False,
            'game_over': False,
            'winning_combination': self.winning_combination,
            'guess_history': []
        }

    def generate_combination(self):
        '''
        Calls RandomNumberService module in ./utils/services  to generate a random combination of 4 numbers using random.org api.
        '''
        service = RandomNumberService()
        return service.fetch_random_numbers()

    def start_game(self):
        '''
        Starts a new game by generating a new winning combination and initializing the game state.
        '''
        self.winning_combination = self.generate_combination()
        self.game_state = self.init_game_state()
        self.save_game()  # Store in Redis Cache
        print(
            f"Game started with ID {self.game_id}, Winning Combination: {self.winning_combination}")

    def process_guess(self, user_guess):
        correct_positions = [i for i in range(
            4) if user_guess[i] == self.winning_combination[i]]
        correct_count = len(correct_positions)
        correct_position = correct_count

        unmatched_winning = [self.winning_combination[i]
                             for i in range(4) if i not in correct_positions]
        unmatched_guess = [user_guess[i]
                           for i in range(4) if i not in correct_positions]

        for digit in unmatched_guess:
            if digit in unmatched_winning:
                correct_count += 1
                unmatched_winning.remove(digit)

        print(f"Processing guess: {user_guess}")
        print(
            f"Correct Count: {correct_count}, Correct Position: {correct_position}")
        return correct_count, correct_position

    def update_game_state(self, user_guess, correct_count, correct_position):
        '''
        '''
        if not self.game_state:
            return False

        self.game_state['last_guess'] = user_guess
        self.game_state['attempts'] += 1

        if correct_position == 4:
            self.game_state['win_state'] = True
            self.game_state['game_over'] = True
        elif self.game_state['attempts'] >= 10:
            self.game_state['game_over'] = True

        guess_record = {
            'guess': user_guess,
            'correct_count': correct_count,
            'correct_position': correct_position
        }

        self.game_state['guess_history'].append(guess_record)

        self.save_game()
        return self.game_state['game_over']

    def end_game(self, request):
        '''
        Performs cleanup and redirects based o win or loss.
        '''

        if self.game_state['win_state']:
            template = 'win.html'
        else:
            template = 'lose.html'

        cache.delete(self.game_id)  # Delete game state from cache

        return render(request, template)
