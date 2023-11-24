from .game_class import Game
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import GuessForm, UserCreationForm, AuthenticationForm
from .models import GameRecord


@login_required(login_url='/login/')
def home(request):
    '''
    Display the home page and the last 5 games played by the user.
    '''
    user_games = GameRecord.objects.filter(user=request.user).order_by(
        '-date')[:5]  # Fetch only the last 5 games; maybe implement pagination later
    context = {
        'user_games': user_games,
    }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def start_game(request):
    '''
    Start a new game and store game state in session
    '''
    game = Game()
    game.start_game()
    request.session['game_id'] = game.game_id
    return HttpResponseRedirect('/game/')


@login_required(login_url='/login/')
def game_board(request):
    '''
    Main board where the user can play the game.
    '''
    game_id = request.session.get('game_id')
    if not game_id:
        # Redirect to home if game_id not found in session
        return HttpResponseRedirect('/')

    game = Game.load_game_state(game_id)
    if not game:
        # Redirect to home if no game state is found
        return HttpResponseRedirect('/')

    form = GuessForm(request.POST or None)
    hint = None

    if form.is_valid():
        user_guess = form.cleaned_data['guess']
        correct_count, correct_position = game.process_guess(user_guess)
        game_over = game.update_game_state(
            user_guess, correct_count, correct_position)

        # Generate a hint if the user has made 5 attempts
        if game.game_state.get('attempts') > 5:
            hint = game.generate_hint()

        # If the game is over, redirect to resolve game
        if game_over:
            return HttpResponseRedirect('/resolve_game/')

        context = {
            'form': form,
            'last_guess': game.game_state.get('last_guess'),
            'correct_count': correct_count,
            'correct_position': correct_position,
            'guess_history': game.game_state.get('guess_history'),
            'attempts': game.game_state.get('attempts'),
            'game_id': game_id,
            'hint': hint,
            'winning_combination': game.winning_combination,
        }
        return render(request, 'game.html', context)

    context = {
        'form': form,
        'game_id': game_id,
    }
    return render(request, 'game.html', context)

# Resolve the game and create a record of the outcome


@login_required(login_url='/login/')
def resolve_game(request):
    game_id = request.session.get('game_id')
    if not game_id:
        return HttpResponseRedirect('/')

    game = Game.load_game_state(game_id)
    if game:
        if request.user.is_authenticated:
            # Create a new GameRecord instance
            if game.game_state.get('win_state'):
                win = True
            else:
                win = False
            GameRecord.objects.create(
                user=request.user,
                game_id=game_id,
                win=win
            )

        return game.resolve_game(request)
    else:
        return HttpResponseRedirect('/')  # Redirect to home if game not found.


# @login_required(login_url='/login/')
# def game_history(request):
#     user_games = GameRecord.objects.filter(user=request.user).order_by('-date')
#     context = {
#         'user_games': user_games,
#     }
#     return render(request, 'home', context)


@login_required(login_url='/login/')
def quit_game(request):
    game_id = request.session.get('game_id')
    if game_id:
        game = Game.load_game_state(game_id)
        if game:
            if request.user.is_authenticated:
                # Count as a Loss
                GameRecord.objects.create(
                    user=request.user,
                    game_id=game_id,
                    win=False
                )
            game.end_game()  # End the game
        del request.session['game_id']  # Delete the game_id from session

    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')
