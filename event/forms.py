from django import forms
from .models import Event

class EventCreationFormSingle(forms.ModelForm):
    class Meta:
        importance_rank = [
        ("1", "Very Important"), 
        ("2", "Important"),
        ("3", "Normal"),
        ]
        model = Event
        fields = ['date', 'start_time', 'end_time', 'text', 'importance']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',}),
            'start_time': forms.TimeInput(attrs={'type': 'time',}),
            'end_time': forms.TimeInput(attrs={'type': 'time',}),
            'importance': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Rank'})
        }
    