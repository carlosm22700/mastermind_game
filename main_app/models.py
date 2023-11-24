from django.db import models
from django.conf import settings


class GameRecord(models.Model):
    '''
    Model to store the game records of each user
    '''
    game_id = models.UUIDField()  # To store the UUID from the Game class
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    win = models.BooleanField()  # True if the user won the game, False if they lost
    # Timestamp for when the game was played
    date = models.DateTimeField(auto_now_add=True)
