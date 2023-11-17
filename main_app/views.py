from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from main_app.serializers import GroupSerializer, UserSerializer

from random import randrange


# Create your views here.


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


def generate_win_condition():
    # create a list to hold win
    win_condition = []

    while (len(win_condition) < 4):  # loops until the length of win_condition is greater than 4
        random_int = randrange(10)
        # add random int to win condition when game begins.
        win_condition.append(str(random_int))

    return win_condition
