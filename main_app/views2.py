import uuid
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .utils.services import RandomNumberService

from .forms import GuessForm


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
        'winning_combinations': winning_combination,
        'guess_history': []
    }
    return game_state


def game():
    # create a new instance of the game state.
    game_state = init(winning_combination)
    # create a unique game id and add to game_state

    # allow user to enter a guess by clicking button

    # check if guess is correct

    # if guess is correct, end game and display win message

    # else if guess is incorrect, and user is on 11th attempt then end game and display lose message

    # else if guess is incorrect, and user is on less than 11th attempt then add attempt to guess history and allow user to enter another guess


def start_game():
    '''
    Starts a new game.
    Generates a unique game ID and initializes the game state.
    Stores the game state in Redis.
    '''
    game_id = str(uuid.uuid4())  # Generate a unique UUID for the game
    game_state = init(winning_combination)  # initialize the game state

    # Here we can stroe the game state in Redis using the game_id as key
    cache.set(game_id, game_state, timeout=3600)  # None for persistent storage

    return game_id, game_state  # Return the game Id and the initialied state


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
    # Responsile for analyzing the user's guess and provide feedback on its accuracy.
    # Returns a tuple (correct_count, correct_position)
    correct_count = 0
    correct_position = 0
    for i in range(4):
        if user_guess[i] == winning_combination[i]:
            correct_position += 1
            correct_count += 1
        elif user_guess[i] in winning_combination:
            correct_count += 1

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

    # Check for win condition
    if user_guess == winning_combination:
        game_state['win_state'] = True
        game_state['game_over'] = True

    elif game_state['attempts'] >= game_state['max_attempts']:
        game_state['game_over'] = True

    # Add the guess record to the guess history
    game_state['guess_history'].append(guess_record)

    cache.set(game_id, game_state, timeout=3600)

    return game_state['game_over']


def end_game(game_id, game_state):
    # Perform any necessary cleanup
    # Redirect based on win or loss
    if game_state['win_state']:
        # return redirect('win')
        pass
    else:
        # return redirect('lose')
        pass

    cache.delete(game_id)  # Delete the game state from the cache

# def check_win_condition(user_guess, winning_combination):
#     '''
#     Compares the user's guess against the winning combination.
#     Returns True if the user has guessed correctly, False otherwise.
#     '''
#     return user_guess == winning_combination


# def check_win_state(game_state):
#     # check for a win
#     if game_state['win_state']:  # returns True if game is won
#         return True

#     # Check for game over due to attempts exhausted
#     if game_state['attempts'] >= game_state['max_attempts']:
#         return True

#     # If neither condition is met, the game continues
#     return False
