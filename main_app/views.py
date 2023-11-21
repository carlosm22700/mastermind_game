import uuid
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .utils.services import RandomNumberService

from .forms import GuessForm


class MastermindGame:
    def __init__(self, session_id):
        self.session_id = session_id
        self.max_attempts = 10
        self._load_game_state()

    '''
    ## I think game state needs to be rechecked to end or continue game... but idk
    '''

    def _load_game_state(self):
        # try to load the game state from the cache
        # will return true if a game is already in session and saved in cache
        game_state = cache.get(self.session_id)
        if game_state:
            # Set the game state from cache
            self.winning_combinations, self.attempts, self.win_state = game_state
            # Debug line to check if game state is loaded correctly:
            print(
                f"Debug: Game state loaded from cache: {self.winning_combinations}, {self.attempts}, {self.win_state}")
        else:
            # Initialize the game state from cache
            service = RandomNumberService()  # create instance of RandomNumberService class
            # call api to generate array of 4 random integers (0-7)
            self.winning_combinations = service.fetch_random_numbers()
            # Debug line
            print(
                f"Debug: New game started with winning combination: {self.winning_combinations}")
            self.attempts = 0  # reset number of attempts to 0
            self.max_attempts = 10
            self.win_state = False  # If won: True; if game lost/in progress: False
            self._save_game_state()

    def _save_game_state(self):
        # Save the game state to the cache
        game_state = (self.winning_combinations, self.attempts, self.win_state)
        # Timeout can be adjusted
        cache.set(self.session_id, game_state, timeout=3600)

    def process_guess(self, user_guess):
        # Convert user_guess string to a list of integers
        user_guess_list = [int(num) for num in user_guess]

        correct_count = 0
        correct_position = 0

        for i in range(4):
            if user_guess_list[i] == self.winning_combinations[i]:
                correct_position += 1
                correct_count += 1
            elif user_guess_list[i] in self.winning_combinations:
                correct_count += 1

        self.attempts += 1
        # Debugging line
        print(
            f"Debug: Attempts: {self.attempts}, Max attempts: {self.max_attempts}")
        self._save_game_state()  # Save updated state

        return correct_count, correct_position

    def check_win(self, user_guess):
        return user_guess == self.winning_combinations

# Start a new game


def start_game(request):
    session_id = str(uuid.uuid4())
    game = MastermindGame(session_id)
    request.session['session_id'] = session_id  # Store session_id in session
    return redirect('home')  # Redirect to home to display the game

# Make a guess


def make_guess(request):
    if request.method == 'POST' and 'session_id' in request.session:
        form = GuessForm(request.POST)
        if form.is_valid():
            user_guess = form.cleaned_data['guess']  # Get guess from form
            print(f"Debug: User guess is {user_guess}")  # Debugging line

            session_id = request.session.get('session_id')
            if session_id:
                game = MastermindGame(session_id)

                if not check_attempts(game):
                    request.session['game_over'] = True
                    request.session['win'] = False
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                correct_count, correct_position = game.process_guess(
                    user_guess)
                # Debugging line
                print(
                    f"Debug: Correct count: {correct_count}, Correct position: {correct_position}")

                # Store results in session
                request.session['last_guess'] = user_guess
                request.session['correct_count'] = correct_count
                request.session['correct_position'] = correct_position

                # Check for a win
                if game.check_win(user_guess):
                    requst.session['game_over'] = True
                    request.session['win'] = True

        else:
            request.session['error'] = "Invald input. Please enter four numbers (0-7)."
            # Redirect back to the home page to display the results
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# Reset game


def reset_game(request):
    # Reset only game-related session keys
    for key in ['session_id', 'last_guess', 'correct_count', 'correct_position', 'game_over', 'win']:
        if key in request.session:
            del request.session[key]

    return redirect('home')


def home(request):
    context = {
        'session_id': request.session.get('session_id'),
        'last_guess': request.session.get('last_guess'),
        'correct_count': request.session.get('correct_count'),
        'correct_position': request.session.get('correct_position'),
        'form': GuessForm(),
    }
    return render(request, 'home.html', context)


def check_attempts(game):
    return game.attempts <= game.max_attempts
