from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nombre', 'fecha', 'configuracion']
        widgets = {
            'configuracion': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }
