from django.core.cache import cache

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions


from .serializers import GroupSerializer, UserSerializer

# from main_app.api_views import StartGameView, MakeGuessView, EndGameView

from main_app.utils.services import RandomNumberService

# Create views here.


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MastermindGame:
    def __init__(self, session_id):
        self.session_id = session_id
        self._load_game_state()

    def _load_game_state(self):
        # try to load the game state from the cache
        game_state = cache.get(self.session_id)
        if game_state:
            # Set the game state from cache
            self.winning_combinations, self.attempts, self.win_state = game_state
        else:
            # Initialize the game state from cache
            service = RandomNumberService()  # create instance of RandomNumberService class
            # call api to generate array of 4 random integers (0-7)
            self.winning_combinations = service.fetch_random_numbers()
            self.attempts = 0  # reset number of attempts to 0
            self.max_attempts = 10
            self.win_state = False  # If won: True; if game lost/in progress: False
            self._save_game_state()

    def _save_game_state(self):
        # Save the game state to the cace
        game_state = (self.winning_combinations, self.attempts, self.win_state)
        # Timeout can be adjusted
        cache.set(self.session_id, game_state, timeout=3600)

    def process_guess(self, user_guess):
        correct_count = 0
        correct_position = 0

        for i in range(4):
            if user_guess[i] == self.winning_combinations[i]:
                correct_position += 1
                correct_count += 1
            elif user_guess[i] in self.winning_combinations:
                correct_count += 1

        self.attempts += 1
        self._save_game_state()  # Save updated state

        return correct_count, correct_position

    def check_win(self, user_guess):
        return user_guess == self.winning_combinations
