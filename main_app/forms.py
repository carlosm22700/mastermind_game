from django import forms

# forms.py
from django import forms


class GuessForm(forms.Form):
    guess = forms.CharField(max_length=4, min_length=4)

    def clean_guess(self):
        data = self.cleaned_data['guess']
        if not all(c.isdigit() and c in '01234567' for c in data):
            raise forms.ValidationError(
                "Invalid input. Enter four numbers (0-7).")
        return data
