import uuid
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .utils.services import RandomNumberService
from random import randint as rand

from .forms import GuessForm


class Game:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.winning_combination = []
        self.game_state = {}  # Initialize an empty game state

    # decorator indicates that this method does not need an instance of the class to be called and lets you load a game state from cache without needing an existing 'Game' Object.
    @staticmethod
    def load_game_state(game_id):
        '''
        Loads the game state from the cache based on the provided game ID.
        :param game_id: str.  The unique identifier for the game.
        :return: Game object if the game state exists, else None.
        '''
        game_state = cache.get(game_id)
        if game_state:
            game = Game()
            game.game_id = game_id
            game.game_state = game_state
            game.winning_combination = game_state['winning_combination']
            return game
        return None

    def save_game(self):
        '''
        Saves the current game state to the cache.
        '''
        cache.set(self.game_id, self.game_state, timeout=3600)

    def init_game_state(self):
        '''
        Initializes the game state wiht default values.
        :return: dict. The initialized game state.
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
        Calls RandomNumberService module in ./utils/services to generate a random combination of 4 numbers using random.org api.
        :return: list. A list of 4 randomly generated numbers.
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
        '''
        Processes the user's guess, comparing it against the winning combination.
        :param user_guess: list. The user's guess, a list of 4 integers.
        :return: tuple. A tuple containing the count of correct numbers and the count of numbers in the correct position.
        '''

        correct_positions = [i for i in range(
            4) if user_guess[i] == self.winning_combination[i]]
        correct_count = len(correct_positions)
        correct_position = correct_count

        # Create lists of unmatched digits
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
        Updates the game state based on the user's guess and the result of processing that guess.
        :param user_guess: list. The user's guess.
        :param correct_count: int. The number of correct digits guessed.
        :param correct_position: int. The number of digits in the correct position.
        :return: bool. True if the game is over, False otherwise.
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

    def generate_hint(self):
        '''
        Generates a hint by revealing one of the digits in the winning combination.
        :return: str. A hint message containing one of the digits from the winnig combination.
        '''
        i = rand(0, 3)
        return "One of the digits is " + str(self.winning_combination[i])

    def resolve_game(self, request):
        '''
        Performs cleanup and redirects based o win or loss status.
        :param request: HttpRequest. The request object.
        :return: HttpResponse. The rendered response for the win or loss page.
        '''

        if self.game_state['win_state']:
            template = 'win.html'
        else:
            template = 'lose.html'

        self.end_game()

        return render(request, template)

    def end_game(self):
        '''
        Deletes the game state from cache.
        :return: bool. The result of the cache deletion operation.
        '''
        return cache.delete(self.game_id)  # Delete game state from cache
