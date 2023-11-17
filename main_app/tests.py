from django.test import TestCase
from main_app.views import generate_win_condition

# Create your tests here.


class GenerateWinConditionTestCase(TestCase):

    def test_win_condition_length(self):
        win_condition = generate_win_condition()
        # Check if the length is exactly 4
        self.assertEqual(len(win_condition), 4)

    # condition does not need to be unique
    # def test_win_condition_uniqueness(self):
    #     win_condition = generate_win_condition()
    #     self.assertEqual(len(win_condition), len(
    #         set(win_condition)))  # Check for uniqueness
