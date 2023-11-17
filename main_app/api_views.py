from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import GroupSerializer, UserSerializer
from .views import MastermindGame

from django.contrib.auth.models import User, Group


import uuid


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


class StartGameView(APIView):
    def post(self, request, *args, **kwargs):
        session_id = str(uuid.uuid4())  # Generate unique session ID
        game = MastermindGame(session_id)  # initialize the game
        return Response({'session_id': session_id}, status=status.HTTP_200_OK)


class MakeGuessView(APIView):
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        user_guess = request.data.get('user_guess')

        if session_id is None or user_guess is None:
            return Response({'error': 'Missing session ID or user guess'}, status=status.HTTP_400_BAD_REQUEST)

        game = MastermindGame(session_id)
        correct_count, correct_position = game.process_guess(user_guess)
        if game.attempts >= game.max_attempts or game.check_win(user_guess):
            game_over = True
        else:
            game_over = False

        response_data = {
            'correct_count': correct_count,
            'correct_position': correct_position,
            'game_over': game_over,
            'win_state': win_state,
            'attempts': game.attempts,
            'max_attempts': game.max_attempts
        }
        return Response(response_data, status=status.HTTP_200_OK)


class EndGameView(APIView):
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')

        if session_id:
            cache.delete(session_id)
            return Response({'message': 'Game ended successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid session ID'}, status=status.HTTP_400_BAD_REQUEST)

        # user_guess = request.data.get('user_guess')
        # game = MastermindGame(session_id)
        # game.check_win(user_guess)
        # return Response({
        #     'win_state': game.win_state,
        #     'winning_combinations': game.winning_combinations
        # }, status=status.HTTP_200_OK)
