# Import Game class from Game.py
from .game_class import Game
from .forms import GuessForm

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def start_game(request):
    game = Game()
    game.start_game()
    request.session['game_id'] = game.game_id
    return HttpResponseRedirect('/game/')


def game_board(request):
    game_id = request.session.get('game_id')
    if not game_id:
        return HttpResponseRedirect('/')

    game = Game.load_game_state(game_id)
    if not game:
        return HttpResponseRedirect('/')

    form = GuessForm(request.POST or None)
    if form.is_valid():
        user_guess = [int(digit) for digit in form.cleaned_data['guess']]
        correct_count, correct_position = game.process_guess(user_guess)
        game_over = game.update_game_state(
            user_guess, correct_count, correct_position)

        if game_over:
            return HttpResponseRedirect('/end_game/')

        context = {
            'form': form,
            'last_guess': game.game_state.get('last_guess'),
            'correct_count': correct_count,
            'correct_position': correct_position,
            'guess_history': game.game_state.get('guess_history'),
            'attempts': game.game_state.get('attempts'),
            'game_id': game_id,
        }
        return render(request, 'game.html', context)

    context = {
        'form': form,
        'game_id': game_id,
    }
    return render(request, 'game.html', context)


def end_game(request):
    game_id = request.session.get('game_id')
    if not game_id:
        return HttpResponseRedirect('/')

    game = Game.load_game_state(game_id)
    if game:
        return game.end_game(request)
    else:
        return HttpResponseRedirect('/')  # Redirect to home if game not found.
