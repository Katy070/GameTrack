from django import forms
from .models import Game, GameStatus


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'release_date', 'genre', 'platform', 'developer', 'cover_image']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GameStatusForm(forms.ModelForm):
    class Meta:
        model = GameStatus
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }