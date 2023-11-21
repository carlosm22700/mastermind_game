import uuid
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .utils.services import RandomNumberService

from .forms import GuessForm


def home(request):
    '''
    Home view - starting point for the game.
    '''
    return render(request, 'home.html')


def generate_combination():
    '''
    Calls RandomNumberService module in ./utils/services  to generate a random combination of 4 numbers using random.org api.
    '''
    service = RandomNumberService()
    return service.fetch_random_numbers()


winning_combination = generate_combination()


def init(winning_combination):
    '''
    Initializes the game state.
    '''
    game_state = {
        'last_guess': [],
        'attempts': 0,
        'win_state': False,
        'game_over': False,
        'winning_combination': winning_combination,
        'guess_history': []
    }
    return game_state


def start_game(request):
    '''
    Starts a new game.
    Generates a unique game ID and initializes the game state.
    Stores the game state in Redis.
    '''
    game_id = str(uuid.uuid4())  # Generate a unique UUID for the game
    game_state = init(winning_combination)  # initialize the game state

    cache.set(game_id, game_state, timeout=3600)  # Store in Redis
    request.session['game_id'] = game_id  # Store the game ID in the session

    return HttpResponseRedirect('/game/')  # Redirect to game board


def game_board(request):
    game_id = request.session.get('game_id')
    if not game_id:
        return HttpResponseRedirect('/')

    game_state = cache.get(game_id)
    if not game_state:
        return HttpResponseRedirect('/')

    form = GuessForm(request.POST or None)
    if form.is_valid():
        user_guess = cleanup_guess(form.cleaned_data['guess'])
        if validate_guess(user_guess):
            correct_count, correct_position = process_guess(
                user_guess, game_state['winning_combination'])
            game_over = update_game_state(
                game_id, user_guess, correct_count, correct_position)

            # Re-fetch the updated game state
            game_state = cache.get(game_id)

            # Print the entire game state or specific parts for debugging
            print("Updated Game State:", game_state)

            if game_over:
                return HttpResponseRedirect('/end_game/')

            print("POST Request - Guess History:",
                  game_state.get('guess_history'))

            context = {
                'form': form,
                'last_guess': game_state.get('last_guess'),
                'correct_count': game_state.get('correct_count'),
                'correct_position': game_state.get('correct_position'),
                'guess_history': game_state.get('guess_history'),
                'game_id': game_id,
            }
            return render(request, 'game.html', context)

    # Default context for initial GET request or if form is not valid
    context = {
        'form': form,
        'last_guess': game_state.get('last_guess'),
        'correct_count': game_state.get('correct_count'),
        'correct_position': game_state.get('correct_position'),
        'guess_history': game_state.get('guess_history'),
        'game_id': game_id,
    }
    return render(request, 'game.html', context)


def make_guess(game_id, user_guess):
    pass


def cleanup_guess(user_guess):
    '''
    Takes guess input and prepares for validation
    return a list of 4 integers.
    '''
    return [int(digit) for digit in user_guess]


def validate_guess(user_guess):
    '''
    Checks if the guess is valid (e.g., correct length, valid numbers).
    Expect a list of integers.
    Returns True if valid, False otherwise.
    '''
    for num in user_guess:
        if num not in range(8):  # check if each digit is in range 0-7
            return False
        elif len(user_guess) != 4:  # check if guess is 4 digits long
            return False

    return True


def process_guess(user_guess, winning_combination):
    correct_positions = [i for i in range(
        4) if user_guess[i] == winning_combination[i]]
    correct_count = len(correct_positions)
    correct_position = correct_count

    # Create copies of the lists to remove matched digits
    unmatched_winning = [winning_combination[i]
                         for i in range(4) if i not in correct_positions]
    unmatched_guess = [user_guess[i]
                       for i in range(4) if i not in correct_positions]

    for digit in unmatched_guess:
        if digit in unmatched_winning:
            correct_count += 1
            # Remove matched digit to prevent double counting
            unmatched_winning.remove(digit)

    return correct_count, correct_position


def update_game_state(game_id, user_guess, correct_count, correct_position):
    # Retrieves the game state from the cache
    # Updates the game state with the new gameand results
    # Saves the updates state back tot he cache
    game_state = cache.get(game_id)

    # If the game state is not found (expired or not started), handle appropriately

    if not game_state:
        return False  # Game state not found

    # Update the game state
    game_state['last_guess'] = user_guess
    game_state['attempts'] += 1

    # Update the guess history with the latest guess and its evaluation
    guess_record = {
        'guess': user_guess,
        'correct_count': correct_count,
        'correct_position': correct_position
    }
    game_state['guess_history'].append(guess_record)

    # Check for win condition
    if user_guess == winning_combination:
        game_state['win_state'] = True
        game_state['game_over'] = True

    elif game_state['attempts'] >= 10:
        game_state['game_over'] = True

    # Add the guess record to the guess history

    cache.set(game_id, game_state, timeout=3600)

    return game_state['game_over']


def end_game(request):
    # Perform any necessary cleanup
    # Redirect based on win or loss
    game_id = request.session.get('game_id')
    if not game_id:
        return HttpResponseRedirect('/')  # Redirect to home if no game_id

    game_state = cache.get(game_id)
    if game_state.get('win_state'):
        template = 'win.html'
    else:
        template = 'lose.html'

    cache.delete(game_id)  # Delete the game state from the cache
    del request.session['game_id']  # Delete the game ID from the session

    return render(request, template)
