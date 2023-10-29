from django import forms
from django.core.exceptions import ValidationError

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('ranking', 'text')
        labels = {
            'ranking': 'Насколько вам понравился маршрут?',
            'text': 'Поделитесь впечатлениями о прогулке (при желании)'
        }

    def clean(self):
        super().clean()
        ranking = self.cleaned_data.get('ranking')
        text = self.cleaned_data.get('text')
        if ranking is None and text.strip() == '':
            raise ValidationError('Вы должны заполнить хотя бы одно поле')
